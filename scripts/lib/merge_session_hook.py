#!/usr/bin/env python3
"""Wires the session-start hook into a project's .claude/settings.json without
clobbering whatever else already lives there. Idempotent: the hook entry is added
once; running again leaves the file unchanged."""
import json
import sys
from pathlib import Path

HOOK_COMMAND = "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: merge_session_hook.py <path-to-settings.json>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    data = {}
    if path.exists():
        text = path.read_text().strip()
        if text:
            data = json.loads(text)

    hooks = data.setdefault("hooks", {})
    session_start = hooks.setdefault("SessionStart", [])
    for entry in session_start:
        for h in entry.get("hooks", []):
            if h.get("command") == HOOK_COMMAND:
                return 0  # already wired

    session_start.append({"hooks": [{"type": "command", "command": HOOK_COMMAND}]})
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
