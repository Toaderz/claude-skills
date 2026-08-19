#!/usr/bin/env bash
#
# Report the real context footprint of each plugin.
#
# Wraps `claude plugin details`, which computes a component inventory and a
# projected token cost statically and locally — no network call, no cost.
#
# The reported number is what the CLI reports. It is not adjusted, rounded
# toward a target, or replaced with an estimate. If a plugin exceeds the
# USER-scope target in docs/architecture.md, the fix is to move its
# highest-cost/lowest-value capability to PROJECT scope or reduce its metadata
# and measure again — not to delete useful capabilities to hit a number.
#
# Usage:  scripts/measure.sh [plugin-name ...]
#         with no arguments, measures every plugin declared in the marketplace.

set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

if ! command -v claude >/dev/null 2>&1; then
  echo "claude CLI not found — cannot measure." >&2
  exit 1
fi

TARGETS=("$@")
if [ "${#TARGETS[@]}" -eq 0 ]; then
  if [ -f .claude-plugin/marketplace.json ]; then
    mapfile -t TARGETS < <(
      python3 -c "
import json
m = json.load(open('.claude-plugin/marketplace.json'))
for p in m.get('plugins', []):
    print(p['name'])
"
    )
  fi
fi

if [ "${#TARGETS[@]}" -eq 0 ]; then
  echo "No plugins declared in the marketplace yet." >&2
  exit 0
fi

printf '\033[1mContext footprint\033[0m\n'
printf 'Target for the USER-scope core: <=600 ambient tokens (a target, not a runtime limit).\n'

for name in "${TARGETS[@]}"; do
  printf '\n\033[1m==> %s\033[0m\n' "$name"
  if ! out=$(claude plugin details "$name" 2>&1); then
    printf '    not installed. Install it first:\n'
    printf '      claude plugin marketplace add ./\n'
    printf '      claude plugin install %s@ai-engineering-os --scope local\n' "$name"
    printf '    CLI said: %s\n' "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
    continue
  fi
  printf '%s\n' "$out" | sed 's/^/    /'
done

printf '\nRecord the measured values in docs/routing-tests.md.\n'
