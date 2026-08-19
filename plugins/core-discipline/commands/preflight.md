---
description: Plan a task before executing it — scope, risks, agent budget, simplest viable approach
argument-hint: [what you want to do]
---

Produce a preflight plan for the following work, following the `preflight-planning`
skill. Do **not** start implementing.

**Task:** $ARGUMENTS

If the task above is empty, plan the work most recently under discussion.

Show the plan. Since this was invoked explicitly, the user wants to see it:

1. **Objective** — one sentence.
2. **Scope** — what is in, and explicitly what is out.
3. **Constraints** — what cannot change.
4. **Assumptions** — and which one is riskiest, plus how to check it in under a minute.
5. **Approach** — which one and why, including the simpler alternative you rejected
   and the reason.
6. **Agent budget** — a number, starting from zero. If it is not zero, give each
   agent a mission and a stopping condition. If it is zero, say so; that is the
   expected answer for most tasks.
7. **Steps** — three to six, each actionable, each naming the files it touches.
8. **Risks** — from the pre-mortem: where this most likely breaks, and what would
   force a redo.
9. **Confidence** — high, medium, or low. If low, say which assumption must be
   validated before any work starts.

Read `.claude/memory/` first if it exists, and search the codebase for existing
implementations before proposing new code. Say so if you find something that already
does most of this.

Then stop and wait. The plan is the deliverable.
