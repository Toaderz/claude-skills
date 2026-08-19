# Capability registry

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

## Active

### `core-discipline` — USER scope

Installed once; applies to every project.

| Capability | Type | Purpose |
|---|---|---|
| `preflight-planning` | skill | Plan non-trivial work before executing it: objective, scope, constraints, risks, agent budget, and the simplest implementation that satisfies the requirement. |
| `project-memory` | skill | Read and write durable project knowledge in .claude/memory/ so decisions, constraints, and lessons survive across sessions. |
| `critical-reviewer` | agent | Adversarial review in an isolated context: try to prove the implementation is wrong. Read-only by construction so it cannot fix a problem and then declare the work sound. |
| `/preflight` | command | Explicit entry point for preflight-planning. Produces a visible plan and stops. |

**Replaces**

- `preflight-planning` ← Claude_optimization/execution-planning.md
- `preflight-planning` ← workflow-orchestrator/SKILL.md (skill-selection and task-classification role)
- `preflight-planning` ← project-structure-governor/SKILL.md (workflow-governance role)
- `project-memory` ← Claude_optimization/memory.md
- `project-memory` ← Claude_optimization/pattern-learning.md

**Notes**

- **`preflight-planning`** — Consolidates the four competing orchestrators. Claude_optimization/pulse-token-efficiency-compactor.md is NOT absorbed and is not claimed as replaced: only its 'budget the context you load' idea survives, as one line in the agent budget. Its reading strategies duplicate guidance the Read tool already gives natively, and its code-compaction rules are generic style advice that was never invocable — the file had no frontmatter at all.

### `engineering` — PROJECT scope

Installed per project, where the work actually lives.

| Capability | Type | Purpose |
|---|---|---|
| `python-dev-discipline` | skill | Disciplined Python development: general heuristics over hardcoded patches, root-cause tracing through the pipeline, stable interfaces, and a regression test before anything is called done. |
| `deep-module-architecture` | skill | Find shallow modules whose interfaces cost as much as their implementations, and propose deepening them so behaviour is tested at one boundary instead of five. |

**Replaces**

- `python-dev-discipline` ← Improve code/develope_code.md
- `deep-module-architecture` ← Improve code/SKILL.md
- `deep-module-architecture` ← Improve code/REFERENCE.md

**Notes**

- **`python-dev-discipline`** — Migrated with the dangling references/advanced_heuristics.md pointer removed — the file never existed and its content is already inline.
- **`deep-module-architecture`** — Renamed from improve-codebase-architecture to avoid colliding with two account-synced copies. gh issue create replaced by mcp__github__issue_write; the mandatory 3-agent fan-out is now conditional on the interface being genuinely contested.

### `architecture` — PROJECT scope

Installed per project, where the work actually lives.

| Capability | Type | Purpose |
|---|---|---|
| `icm-architect` | skill | Design a process, body of knowledge, or codebase into an ICM workspace where folder structure carries the orchestration, or restructure an existing folder into one. |

**Replaces**

- `icm-architect` ← icm-architect/
- `icm-architect` ← project-structure-governor/

**Notes**

- **`icm-architect`** — The 'Auto-use in this account' section and the auto-apply clause in the description were removed: they contradicted the skill's own guardrail that a workspace for something done twice is scaffolding, not architecture. MIT attribution (Van Clief & McDermott) preserved in SOURCE.md and LICENSE.

### `frontend` — PROJECT scope

Installed per project, where the work actually lives.

| Capability | Type | Purpose |
|---|---|---|
| `diseno-web-estrategico` | skill | Strategic web design synthesising three methodologies, with a rule hierarchy: what all three authors agree on is mandatory, what only one mentions is optional with judgement. |
| `ui-ux-review` | skill | Review an interface for what breaks real users: keyboard and screen-reader access, contrast, hierarchy, narrow widths, component structure, and design-system consistency. |

**Replaces**

- `diseno-web-estrategico` ← account-synced diseno-web-estrategico (retire from claude.ai)

**Notes**

- **`diseno-web-estrategico`** — Imported verbatim from the account-synced copy; body left in Spanish deliberately rather than translated, to avoid drift in content this repo did not author. No paths: filter — the skill has to fire before any component file exists.
- **`ui-ux-review`** — Shipped WITHOUT a paths: filter despite the plan calling for one. Issue #49835 can make a paths-scoped skill undiscoverable, and with runtime routing evaluation cost-prohibited there is no way to detect that failure here. The description routes it; paths: is one line to add if wanted.

### `finance` — PROJECT scope

Installed per project, where the work actually lives.

| Capability | Type | Purpose |
|---|---|---|
| `news-prioritization` | skill | Rank macro-financial news by macro impact, surprise, and direct relevance to a tracked investment universe, producing a scored shortlist with one actionable insight each. |

**Replaces**

- `news-prioritization` ← research/SKILL.md
- `news-prioritization` ← research/news-prioritization.skill (ZIP)

**Notes**

- **`news-prioritization`** — Moved to its own finance plugin rather than research, so the generic research plugin stays installable anywhere. The '## Assets (Exact Match)' contract was broken — no such heading exists — and now matches the real sector-heading structure. The universe itself is personal holdings and is NOT bundled: this repository is public, so the plugin ships only a format example and reads the real file from the project. The skill states the gap explicitly when no universe is found instead of scoring portfolio relevance without one.

### `quality` — PROJECT scope

Installed per project, where the work actually lives.

| Capability | Type | Purpose |
|---|---|---|
| `postflight-audit` | skill | Verify finished work before it is called done, at a depth proportional to what the change can break, actively looking for reasons not to approve. |
| `/postflight` | command | Explicit entry point for postflight-audit, with the audit shown rather than applied. |

**Replaces**

- `postflight-audit` ← workflow-orchestrator/SKILL.md §7 final cold verification

**Notes**

- **`postflight-audit`** — Kept out of core-discipline: it is not universal, and the core is already 40 tokens over its target. Promotion to USER scope is a measurement decision, recorded in docs/routing-tests.md.

### `research` — PROJECT scope

Installed per project, where the work actually lives.

| Capability | Type | Purpose |
|---|---|---|
| `deep-research` | skill | Research to a chosen depth with an explicit stopping criterion, ranked source tiers, triangulation of load-bearing claims, and evidence kept separate from interpretation. |
| `decision-comparison` | skill | Compare options against criteria stated before the verdict, mark evidence by how it is known, name the missing data, and recommend or decline to. |

**Notes**

- **`decision-comparison`** — Description anchors on the SHAPE of the request (compare options and recommend), not on a domain, so it serves APIs, architecture, vendors, or hotels without becoming so broad it stops discriminating.

---

## Deferred, with reasons

Recorded so the decisions are not silently relitigated. Adding either requires passing the gate in [`../docs/capability-policy.md`](../docs/capability-policy.md) with written justification.

| Candidate | Type | Why not |
|---|---|---|
| `security-auditor` | agent | Duplicates the built-in /security-review, which is already maintained upstream. postflight-audit invokes the built-in instead. Build only if the built-in proves insufficient, and record that finding first. |
| `test-engineer` | agent | Context isolation is a cost here, not a benefit: an agent that did not see what was just built writes worse tests than the main agent that did. Build only for a case where isolation genuinely helps, such as long noisy suites that would flood the main context. |

---

14 capabilities across 7 plugins. Measured ambient cost per plugin is in [`../docs/routing-tests.md`](../docs/routing-tests.md).
