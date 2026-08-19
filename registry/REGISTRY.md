# Capability registry

Human-readable view of [`registry.json`](registry.json).

> **This is not a router.** Claude never reads the registry to decide what to do.
> Routing is Claude Code's native mechanism: it preloads each skill's `name` and
> `description` and loads the body on match. The registry exists for people —
> discovery, maintenance, auditing, dependency tracking, inventory. A registry read
> into context on every task would be exactly the custom router this architecture
> refuses to build. See [`../docs/architecture.md`](../docs/architecture.md).

`scripts/validate.sh` fails if this and the files on disk disagree.

---

## Active

### `core-discipline` — USER scope

Installed once; applies to every project.

| Capability | Type | Purpose |
|---|---|---|
| `preflight-planning` | skill | Plan non-trivial work before executing: objective, scope, constraints, risks, agent budget, simplest viable implementation. |
| `project-memory` | skill | Durable project knowledge in `.claude/memory/` so decisions and lessons survive across sessions. |
| `critical-reviewer` | agent | Adversarial review in isolated context. Read-only: `Read`, `Grep`, `Glob`. |
| `/preflight` | command | Explicit entry point for planning. Produces a visible plan and stops. |

**What these consolidate.** `preflight-planning` replaces four capabilities that each
claimed to be the top-level orchestrator: `execution-planning`, the skill-selection
role of `workflow-orchestrator`, the workflow-governance role of
`project-structure-governor`, and the reading-discipline and output rules of
`pulse-token-efficiency-compactor`. `project-memory` merges `memory.md` and
`pattern-learning.md`, which overlapped heavily and both depended on a tool and a path
that do not exist — it has a real file backend instead.

---

## Deferred, with reasons

Recorded so the decisions are not silently relitigated. Adding either requires passing
the gate in [`../docs/capability-policy.md`](../docs/capability-policy.md) with written
justification.

| Candidate | Why not |
|---|---|
| `security-auditor` agent | Duplicates the built-in `/security-review`, already maintained upstream. `postflight-audit` invokes the built-in. Build only if the built-in proves insufficient — and record that finding first. |
| `test-engineer` agent | Context isolation is a cost here, not a benefit: an agent that did not see what was just built writes worse tests than the main agent that did. Build only where isolation genuinely helps, such as long noisy suites that would flood the main context. |

---

## Fields

| Field | Meaning |
|---|---|
| `name` | must match the directory name and the frontmatter `name` |
| `type` | `skill`, `agent`, or `command` |
| `plugin` | which plugin ships it — this is also its scope decision |
| `path` | repo-relative; validated to exist |
| `purpose` | one sentence |
| `triggers` | literal phrases, `en` and `es` |
| `excludes` | what it deliberately does not cover — this is what buys routing precision |
| `dependencies` | other capabilities it relies on |
| `required_tools` | the minimum sufficient set |
| `backend` | files or services it reads and writes, where applicable |
| `scope` | `user` or `project` |
| `cost` | context characteristics |
| `replaces` | what it consolidated, so removals stay traceable |
| `status` | `active` or `deprecated` |
| `since` | version introduced |

## Adding an entry

Register the capability in the same commit that adds it, then run
`scripts/validate.sh` — an unregistered skill and a registry entry pointing at a
missing file are both build failures.
