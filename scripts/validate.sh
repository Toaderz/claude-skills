#!/usr/bin/env bash
#
# Validate every manifest, skill, agent, and command in this repository.
#
# Everything here is deterministic, local, and free — no network calls, no paid
# services, nothing with uncertain cost. See docs/architecture.md.
#
# Usage:  scripts/validate.sh
# Exit:   0 clean, 1 problems found.

set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

FAILED=0
step() { printf '\n\033[1m==> %s\033[0m\n' "$1"; }
fail() { printf '\033[31m    FAIL: %s\033[0m\n' "$1"; FAILED=1; }
ok()   { printf '\033[32m    ok: %s\033[0m\n' "$1"; }

# --------------------------------------------------------------- prerequisites

if ! command -v claude >/dev/null 2>&1; then
  echo "claude CLI not found; manifest validation will be skipped." >&2
  HAVE_CLAUDE=0
else
  HAVE_CLAUDE=1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found; repo lint cannot run." >&2
  exit 1
fi

# --------------------------------------------------------------- json syntax

step "JSON syntax"
while IFS= read -r f; do
  if python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$f" 2>/dev/null; then
    ok "$f"
  else
    fail "$f is not valid JSON"
  fi
done < <(find . -name '*.json' -not -path './.git/*' | sort)

# --------------------------------------------------------------- manifests

if [ "$HAVE_CLAUDE" -eq 1 ]; then
  step "Marketplace manifest"
  if out=$(claude plugin validate ./ 2>&1); then
    ok "marketplace"
    [ -n "$out" ] && printf '%s\n' "$out" | sed 's/^/    /'
  else
    fail "marketplace"
    printf '%s\n' "$out" | sed 's/^/    /'
  fi

  step "Plugin manifests (--strict)"
  if [ -d plugins ]; then
    for d in plugins/*/; do
      [ -d "$d" ] || continue
      name="$(basename "$d")"
      if out=$(claude plugin validate "$d" --strict 2>&1); then
        ok "$name"
        [ -n "$out" ] && printf '%s\n' "$out" | sed 's/^/    /'
      else
        fail "$name"
        printf '%s\n' "$out" | sed 's/^/    /'
      fi
    done
  else
    echo "    (no plugins/ directory yet)"
  fi
fi

# --------------------------------------------------------------- repo lint

step "Repository lint"
if ! python3 "$REPO/scripts/lib/lint.py"; then
  FAILED=1
fi

# --------------------------------------------------------------- verdict

printf '\n'
if [ "$FAILED" -eq 0 ]; then
  printf '\033[32mVALIDATION PASSED\033[0m\n'
else
  printf '\033[31mVALIDATION FAILED\033[0m\n'
fi

printf '\nNote: these checks are structural. They do not establish routing precision,\n'
printf 'routing recall, or semantic activation reliability — that needs a runtime\n'
printf 'evaluation, which is not authorized. See docs/architecture.md.\n'

exit "$FAILED"
