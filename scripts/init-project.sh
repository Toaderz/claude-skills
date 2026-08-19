#!/usr/bin/env bash
# Install this library's capabilities into a project, choosing plugins by what the
# project actually contains.
#
# Idempotent: running it twice changes nothing the second time.
# It never overwrites an existing Claude configuration silently — see check_config().
set -uo pipefail

MARKETPLACE_NAME="ai-engineering-os"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

DRY_RUN=0
ASSUME_YES=0
SCOPE="project"
EXPLICIT=""
TARGET="$PWD"

bold=$'\033[1m'; red=$'\033[31m'; green=$'\033[32m'; yellow=$'\033[33m'; off=$'\033[0m'
say()  { printf '%s\n' "$*"; }
info() { printf '  %s\n' "$*"; }
ok()   { printf '  %s%s%s\n' "$green" "$*" "$off"; }
warn() { printf '  %s%s%s\n' "$yellow" "$*" "$off"; }
die()  { printf '%sERROR:%s %s\n' "$red" "$off" "$*" >&2; exit 1; }

usage() {
  cat <<'USAGE'
Usage: init-project.sh [options] [target-directory]

  --only a,b,c   Install exactly these plugins; skip detection entirely.
  --all          Install every plugin. Rarely right — see the cost note below.
  --scope S      user | project | local   (default: project)
  --dry-run      Print what would happen. Change nothing.
  -y, --yes      Do not prompt.
  -h, --help     This text.

Plugins: core-discipline quality engineering architecture frontend research finance

Cost note: every plugin installed is resident in every session for that scope.
Measured always-on: core-discipline ~640, quality ~246, engineering ~478,
frontend ~481, research ~426, architecture ~293, finance ~233 tokens.
--all is ~2,797 tokens in every session, forever. Detection exists to avoid that.
USAGE
}

while [ $# -gt 0 ]; do
  case "$1" in
    --only)
      [ $# -ge 2 ] && [ -n "${2:-}" ] || die "--only needs a plugin list"
      EXPLICIT="$2"; shift 2 ;;
    --all) EXPLICIT="core-discipline,quality,engineering,architecture,frontend,research,finance"; shift ;;
    --scope)
      # Check for the operand BEFORE shifting. `shift 2` with one argument left is an
      # error that shifts nothing, and with no `set -e` the loop re-enters on the same
      # argument forever — `init-project.sh --scope` hung silently.
      [ $# -ge 2 ] && [ -n "${2:-}" ] || die "--scope needs a value: user, project, or local"
      SCOPE="$2"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    -y|--yes) ASSUME_YES=1; shift ;;
    -h|--help) usage; exit 0 ;;
    -*) die "unknown option: $1  (try --help)" ;;
    *) TARGET="$1"; shift ;;
  esac
done

case "$SCOPE" in
  user|project|local) ;;
  *) die "--scope must be user, project, or local (got: '$SCOPE')" ;;
esac

# ---------------------------------------------------------------- preconditions

command -v claude >/dev/null 2>&1 \
  || die "the 'claude' CLI is not on PATH. Install Claude Code first: https://claude.com/claude-code"

[ -d "$TARGET" ] || die "target directory does not exist: $TARGET"
TARGET="$(cd "$TARGET" && pwd)"

[ -f "$REPO_ROOT/.claude-plugin/marketplace.json" ] \
  || die "no marketplace manifest at $REPO_ROOT/.claude-plugin/marketplace.json — is this the library repo?"

# Never clobber an existing configuration without saying so.
check_config() {
  local f="$TARGET/.claude/settings.json"
  [ -f "$f" ] || return 0
  if grep -q "$MARKETPLACE_NAME" "$f" 2>/dev/null; then
    info "existing .claude/settings.json already references $MARKETPLACE_NAME — will add to it, not replace it"
  else
    warn "$TARGET/.claude/settings.json exists and does not mention $MARKETPLACE_NAME."
    warn "The CLI will merge into it. Nothing here rewrites it, but back it up if it matters."
  fi
}

# ---------------------------------------------------------------- detection

detect() {
  local found=()
  local d="$TARGET"

  # core-discipline and quality are not detected: planning, memory, and a
  # completion gate apply to any project that does work at all.
  found+=("core-discipline" "quality")

  if ls "$d"/*.py >/dev/null 2>&1 \
     || [ -f "$d/pyproject.toml" ] || [ -f "$d/requirements.txt" ] || [ -f "$d/setup.py" ] \
     || find "$d" -maxdepth 3 -name '*.py' -not -path '*/.*' -print -quit 2>/dev/null | grep -q .
  then found+=("engineering"); fi

  if [ -f "$d/package.json" ] \
     || find "$d" -maxdepth 3 \( -name '*.tsx' -o -name '*.jsx' -o -name '*.vue' -o -name '*.svelte' \) \
          -not -path '*/node_modules/*' -not -path '*/.*' -print -quit 2>/dev/null | grep -q .
  then found+=("frontend"); fi

  printf '%s\n' "${found[@]}"
}

# research, architecture and finance are deliberately NOT auto-detected. Nothing on
# disk tells you a project does research or follows markets, and guessing installs
# ambient cost the project may never use. Ask for them with --only.

if [ -n "$EXPLICIT" ]; then
  IFS=',' read -r -a PLUGINS <<< "$EXPLICIT"
  SOURCE_OF_CHOICE="explicit (--only/--all)"
else
  mapfile -t PLUGINS < <(detect)
  SOURCE_OF_CHOICE="detected from $TARGET"
fi

VALID="core-discipline quality engineering architecture frontend research finance"
for p in "${PLUGINS[@]}"; do
  case " $VALID " in *" $p "*) ;; *) die "unknown plugin: '$p'. Valid: $VALID" ;; esac
done

# ---------------------------------------------------------------- plan

say ""
say "${bold}Installing into:${off} $TARGET"
say "${bold}Scope:${off} $SCOPE   ${bold}Selection:${off} $SOURCE_OF_CHOICE"
say ""
say "${bold}Plugins${off}"
for p in "${PLUGINS[@]}"; do info "$p"; done
for p in $VALID; do
  case " ${PLUGINS[*]} " in *" $p "*) ;; *) info "skip: $p" ;; esac
done
say ""
check_config

if [ "$DRY_RUN" -eq 1 ]; then
  say ""
  ok "dry run — nothing was changed."
  exit 0
fi

if [ "$ASSUME_YES" -eq 0 ] && [ -t 0 ]; then
  printf '  Proceed? [y/N] '
  read -r reply
  case "$reply" in y|Y|yes|YES) ;; *) say "  aborted."; exit 0 ;; esac
fi

# ---------------------------------------------------------------- execute

cd "$TARGET" || die "cannot enter $TARGET"

say ""
say "${bold}Marketplace${off}"
if claude plugin marketplace list 2>/dev/null | grep -q "$MARKETPLACE_NAME"; then
  ok "already registered: $MARKETPLACE_NAME"
else
  if out=$(claude plugin marketplace add "$REPO_ROOT" --scope "$SCOPE" 2>&1); then
    ok "registered: $MARKETPLACE_NAME"
  else
    say "$out" >&2
    die "could not register the marketplace from $REPO_ROOT"
  fi
fi

say ""
say "${bold}Plugins${off}"
installed_now=0; already=0; failed=0
# Which settings file actually records installs for this scope. Parsing the output of
# `claude plugin list` was wrong: its lines read "> name@marketplace", so the plugin
# never matched and every re-run reported installing what it had not installed. The
# result was still idempotent, but the report was false, which is worse than no report.
case "$SCOPE" in
  project) STATE_FILE="$TARGET/.claude/settings.json" ;;
  local)   STATE_FILE="$TARGET/.claude/settings.local.json" ;;
  user)    STATE_FILE="$HOME/.claude/settings.json" ;;
esac

is_installed() {
  [ -f "$STATE_FILE" ] || return 1
  grep -q "\"$1@$MARKETPLACE_NAME\"[[:space:]]*:[[:space:]]*true" "$STATE_FILE" 2>/dev/null
}

for p in "${PLUGINS[@]}"; do
  if is_installed "$p"; then
    ok "already installed: $p"
    already=$((already + 1))
    continue
  fi
  if out=$(claude plugin install "$p@$MARKETPLACE_NAME" --scope "$SCOPE" --yes 2>&1); then
    ok "installed: $p"
    installed_now=$((installed_now + 1))
  else
    warn "FAILED: $p"
    say "$out" >&2
    failed=$((failed + 1))
  fi
done

say ""
say "${bold}Result${off}"
info "installed now: $installed_now    already present: $already    failed: $failed"

if [ "$failed" -gt 0 ]; then
  die "$failed plugin(s) failed to install. Nothing was rolled back; re-run after fixing the cause."
fi

say ""
info "Verify:   claude plugin list"
info "Cost:     claude plugin details <plugin>"
ok "done."
