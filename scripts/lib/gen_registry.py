#!/usr/bin/env python3
"""Generate registry/REGISTRY.md from registry/registry.json.

REGISTRY.md used to be hand-maintained beside registry.json and claimed the validator
kept them in sync. Nothing read it, so it drifted: it documented one of seven plugins
and asserted a `replaces` that registry.json explicitly disclaimed. One home per fact —
the JSON is the home, this renders it.

  --check   exit 1 if the file on disk differs from what would be generated
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
JSON = REPO / "registry" / "registry.json"
OUT = REPO / "registry" / "REGISTRY.md"

SCOPE_NOTE = {
    "user": "Installed once; applies to every project.",
    "project": "Installed per project, where the work actually lives.",
}

HEADER = """# Capability registry

Human-readable view of [`registry.json`](registry.json).

> **This is not a router.** Claude never reads the registry to decide what to do.
> Routing is Claude Code's native mechanism: it preloads each skill's `name` and
> `description` and loads the body on match. The registry exists for people —
> discovery, maintenance, auditing, dependency tracking, inventory. A registry read
> into context on every task would be exactly the custom router this architecture
> refuses to build. See [`../docs/architecture.md`](../docs/architecture.md).

**Generated from `registry.json` by `scripts/lib/gen_registry.py`. Do not edit by hand** —
`scripts/validate.sh` fails when this file and the JSON disagree.

---
"""


def render() -> str:
    data = json.loads(JSON.read_text(encoding="utf-8"))
    caps = data["capabilities"]

    order, seen = [], set()
    for c in caps:
        if c["plugin"] not in seen:
            seen.add(c["plugin"])
            order.append(c["plugin"])

    out = [HEADER, "\n## Active\n"]
    for plugin in order:
        members = [c for c in caps if c["plugin"] == plugin]
        scope = members[0].get("scope", "project")
        out.append(f"\n### `{plugin}` — {scope.upper()} scope\n")
        out.append(f"\n{SCOPE_NOTE.get(scope, '')}\n")
        out.append("\n| Capability | Type | Purpose |\n|---|---|---|\n")
        for c in members:
            name = f"/{c['name']}" if c["type"] == "command" else c["name"]
            out.append(f"| `{name}` | {c['type']} | {c['purpose']} |\n")

        replaced = [(c["name"], r) for c in members for r in c.get("replaces", [])]
        if replaced:
            out.append("\n**Replaces**\n\n")
            for name, r in replaced:
                out.append(f"- `{name}` ← {r}\n")

        notes = [(c["name"], c["notes"]) for c in members if c.get("notes")]
        if notes:
            out.append("\n**Notes**\n\n")
            for name, n in notes:
                out.append(f"- **`{name}`** — {n}\n")

    if data.get("deferred"):
        out.append("\n---\n\n## Deferred, with reasons\n")
        out.append(
            "\nRecorded so the decisions are not silently relitigated. Adding either "
            "requires passing the gate in "
            "[`../docs/capability-policy.md`](../docs/capability-policy.md) with written "
            "justification.\n"
        )
        out.append("\n| Candidate | Type | Why not |\n|---|---|---|\n")
        for d in data["deferred"]:
            out.append(f"| `{d['name']}` | {d['type']} | {d['reason']} |\n")

    out.append(
        f"\n---\n\n{len(caps)} capabilities across {len(order)} plugins. "
        "Measured ambient cost per plugin is in "
        "[`../docs/routing-tests.md`](../docs/routing-tests.md).\n"
    )
    return "".join(out)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != text:
            print("  ERROR: registry/REGISTRY.md is stale — run scripts/lib/gen_registry.py")
            return 1
        return 0
    OUT.write_text(text, encoding="utf-8")
    print(f"  wrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
