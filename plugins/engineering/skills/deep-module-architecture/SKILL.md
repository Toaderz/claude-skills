---
name: deep-module-architecture
description: >
  Finds where a codebase is made of shallow modules whose interfaces cost nearly as much
  as their implementations, and proposes deepening them so behaviour can be tested at one
  boundary instead of inside five. Use when asked to improve architecture, reduce coupling,
  make code more testable or more navigable, consolidate modules that always change
  together, or on "refactor this", "too many modules", "tight coupling", "hard to test",
  "architecture review", "how should I structure this", "revisa la arquitectura",
  "está muy acoplado", "cómo estructuro esto". Do NOT use for one-off scripts, single bug
  fixes, syntax questions, or ordinary code review — the built-in /code-review covers that.
---

# Deep module architecture

A **deep module** (John Ousterhout, *A Philosophy of Software Design*) has a small
interface hiding a large implementation. Deep modules are more testable, more navigable,
and let you test at the boundary instead of inside.

The goal is not fewer files. It is **less interface per unit of behaviour**.

---

## 1. Explore the codebase

Navigate it the way a newcomer would, and note where you experience friction:

- Where does understanding one concept require bouncing between many small files?
- Where is a module so shallow that its interface is nearly as complex as its body?
- Where were pure functions extracted for testability, while the real bugs live in how
  they are called?
- Where does coupling between modules create risk in the seams?
- What is untested, or hard to test?

**The friction you encounter is the signal.** Do not run a checklist over the tree.

Delegate this to a read-only `Explore` subagent when the codebase is large enough that
sweeping it would flood the main context — that is the one case where isolation pays.
For a codebase you can already see, read it directly.

## 2. Present candidates

A numbered list. For each:

- **Cluster** — which modules or concepts are involved
- **Why they are coupled** — shared types, call patterns, co-ownership of a concept
- **Dependency category** — see [references/dependency-categories.md](references/dependency-categories.md)
- **Test impact** — which existing tests boundary tests would replace

**Do not propose interfaces yet.** Ask which candidate to explore.

## 3. Frame the problem space

Once a candidate is picked, write a plain explanation of it before designing anything:

- The constraints any new interface must satisfy
- The dependencies it must rely on
- A rough code sketch to make the constraints concrete — grounding, not a proposal

## 4. Design the interface

**Default: design it yourself.** One considered interface, with its trade-offs stated,
is usually the deliverable.

Fan out to parallel subagents **only** when the interface is genuinely contested — the
constraints admit real alternatives, and you cannot tell which wins without seeing them
side by side. When that holds, give each agent a different design constraint so the
outputs actually differ:

| Agent | Constraint |
|---|---|
| 1 | Minimise the interface — 1–3 entry points |
| 2 | Maximise flexibility — many use cases, room to extend |
| 3 | Optimise for the most common caller — the default case is trivial |
| 4 | Ports and adapters, if the dependency crosses a network boundary |

Brief each with the technical facts (file paths, coupling details, dependency category,
what is being hidden), not with the user-facing explanation from step 3.

Each design states: interface signature · a usage example · what complexity it hides ·
how dependencies are handled · trade-offs.

**Never fan out because fanning out is available.** Three agents producing three variants
of the same obvious interface is three times the cost for one answer.

## 5. Recommend

Compare the designs in prose, then give your own read: which is strongest and why. If
elements combine well, propose the hybrid. **Be opinionated — a menu is not advice.**

## 6. Write the RFC

Create the refactor RFC as a GitHub issue with `mcp__github__issue_write`, using the
template in [references/dependency-categories.md](references/dependency-categories.md).
Create it and share the URL; do not ask for a review pass first.

If the GitHub MCP tools are not available in the session, **say so and output the RFC as
markdown instead**. Do not fall back to `gh` — it is not guaranteed to be installed, and
a silent failure is worse than a plain report.

---

## Rules

1. Friction is the signal; a checklist is not.
2. Candidates before interfaces. Never design what has not been chosen.
3. One good interface beats a fan-out. Parallel agents are for contested calls only.
4. Replace tests, do not layer them — see the reference.
5. The RFC describes responsibilities and contracts, not current file paths.
