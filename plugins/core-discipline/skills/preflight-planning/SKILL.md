---
name: preflight-planning
description: >
  Plans non-trivial work before executing it — objective, scope, constraints, risks,
  which capabilities apply, an explicit agent budget, and the simplest implementation
  that satisfies the requirement. Use when a request touches more than one file or
  step, when requirements are ambiguous, when several approaches are viable, when a
  previous attempt failed, or when the user says "build", "create", "implement",
  "fix", "refactor", "migrate", "automate", "plan", "how should we", "construye",
  "crea", "implementa", "arregla", "refactoriza", "migra", "automatiza", "planifica",
  "cómo le hacemos". Also use before dispatching any subagent, to decide whether one
  is warranted at all. Do NOT use for single-fact questions, typo fixes, one-line
  edits, reading or explaining a file, or any request the user framed as quick
  ("rápido", "just do it", "nada más dime").
---

# Preflight planning

Plan first, execute once. The cost of planning is a minute; the cost of not planning
is a rewrite.

This skill produces a plan. It does not produce code, and it does not dispatch agents
on its own — deciding whether an agent is warranted is part of the plan.

---

## The gate: does this need a plan at all?

Over-planning trivial work is its own failure mode. Match the depth to the task.

| Signal | Depth |
|---|---|
| Single-line fix, typo, factual question, reading a file | **none** — just do it |
| Clear task, one obvious approach, under 3 steps | **minimal** — plan internally, execute |
| More than one viable approach, or more than 3 steps | **standard** — internal plan, checkpointed execution |
| Ambiguous requirements, high stakes, production surface, or a previous attempt failed | **full** — explicit plan, pre-mortem, controlled execution |
| The user asked for a plan or strategy | **full + visible** — show it |

Plans are **internal by default**. Show one when the task is genuinely complex or
risky, or when asked. Narrating a plan for a two-line change is noise.

**The user can override.** "rápido", "quick", "just do it", "nada más hazlo" drops the
depth one or two levels regardless of complexity. That is their time-quality tradeoff
to make, not yours.

---

## 1. Understand

Before planning, get the task straight:

- **Objective** — one sentence. What does success look like?
- **Scope** — what is in, and explicitly what is out.
- **Constraints** — what cannot change: existing interfaces, file formats, conventions
  already in the codebase, the user's stated preferences.
- **Inputs** — what exists to work with. Verify it exists rather than assuming.
- **Expected output** — format and level of detail.
- **Success criteria** — the condition that means stop.

If the task is ambiguous on a **critical** dimension, ask one focused question. One
question beats one wrong assumption. If it is ambiguous on a non-critical dimension,
choose the obvious default, say which default you chose, and keep moving.

---

## 2. Take stock of what is already known

Check `project-memory` for prior decisions, constraints, and lessons on this codebase
before designing anything. A constraint discovered three sessions ago is cheaper to
recall than to rediscover.

Assemble internally:

```
MUST DO:     from prior decisions and constraints
MUST AVOID:  from recorded lessons and failed approaches
REUSE:       existing functions, utilities, and patterns already in the codebase
```

**Search the codebase for existing implementations before proposing new ones.** Most
"new" code duplicates something already present.

---

## 3. Budget the agents — default is zero

This is the rule that keeps work proportionate.

> **Never dispatch a subagent simply because subagents exist.**

| Task | Agents |
|---|---|
| Simple | **0** — the main agent, working directly |
| Specialized, bounded, benefits from isolation | **1** |
| Two genuinely independent substantial subtasks | **2, in parallel** |
| Complex project that truly decomposes | **N**, and only with the decomposition written down |

Before dispatching any agent, all of these must be true:

1. The work has a clearly defined mission and a stopping condition.
2. **Isolation helps rather than hurts.** Ask this specifically. For adversarial
   review, isolation is the mechanism — the reviewer cannot be anchored by reasoning
   it never saw. For writing tests against code just built, isolation is a cost — an
   agent that did not see the work writes worse tests than the one that did.
3. There is enough work to justify the setup cost.
4. It either parallelizes usefully, or it keeps significant noise out of the main
   context.

If any is false, do the work directly.

**Never "research everything."** Broad speculative fan-out is the most expensive way
to be wrong. Scope each agent to a question with an answer.

Also budget the rest: minimum tools, minimum MCP servers, minimum context loaded.
Optimize for useful work per token and per tool call, not for activity.

---

## 4. Choose an approach

| Approach | Fits | Main risk |
|---|---|---|
| **Direct + validate** | clear, bounded change | skipping the validation |
| **Pipeline** | sequential stages, data flow | stage ordering |
| **Modular decomposition** | independent parts | interface mismatch at integration |
| **Iterative refinement** | fuzzy or quality-dependent target | never converging — cap at 3 passes |
| **Reuse a prior approach** | recurring task solved before | context drift since last time |

Selection: if something similar was solved before, start there. Otherwise pick the
simplest approach that fits the shape of the work.

**Then ask the question that matters most:**

> Is there a simpler implementation that satisfies the actual requirement?

If yes, that is the plan. Scope creep dressed as thoroughness is still scope creep.

---

## 5. Write the plan

```
Objective: one sentence
Approach:  from step 4
Agents:    0, or the list with each one's mission and stopping condition
Steps:
  1. concrete, actionable
  2. concrete, actionable
  3. concrete, actionable
Risks:     from the pre-mortem
```

Rules:

- **3–6 steps.** More than that means the task should be decomposed first.
- **Every step is actionable.** "Understand the data" is not a step. "Read the first
  20 rows and confirm the header row index" is a step.
- **Name the files.** A plan that does not say what it will touch is not a plan.

### Confidence

- **High** — similar work done before, clear requirements, few assumptions → execute.
- **Medium** — reasonable approach with some uncertainty → execute, with a checkpoint
  at each risky step.
- **Low** — significant assumptions, no precedent, unclear requirements → **validate
  the riskiest assumption before executing.**

Do not execute a low-confidence plan. Thirty seconds of checking beats a full redo.

---

## 6. Pre-mortem

The highest-leverage minute in the whole process. Skip it at minimal depth; do it
quickly at standard depth; do it properly at full depth.

1. **Where is this most likely to break?** Check recorded lessons for warning signs
   that match this plan.
2. **What am I assuming?** About data shape, about intent, about library behavior,
   about what the existing code does. Which of those can be checked in ten seconds?
3. **What would force a redo?** Wrong output format, missed edge case, misread
   requirement.

Then adjust: add a validation step where risk is high, reorder so a fragile
dependency fails early, add a checkpoint where the user can confirm before you build
on top of an assumption.

---

## 7. Execute

**Validate the riskiest assumption first.** Before processing data, inspect its actual
structure. Before refactoring, confirm current behavior. Before building on a library,
verify it does what you think. Ten seconds of inspection prevents ten minutes of
rework — and if the assumption is wrong, the plan changes *before* the work, not after.

Then:

- **Follow the plan.** The plan was built with context that improvising throws away.
- **Checkpoint at decisions.** Whenever a step involves a choice, confirm it still
  matches the plan.
- **Notice drift.** Justified by new information → update the plan and continue.
  Unconscious → correct back. The plan itself is wrong → stop and replan.
- **Fail fast.** Unexpected output means stop and diagnose, not continue and hope.
- **Stop when the success criteria are met.** Do not add unrequested features, do not
  refactor what was not asked about, do not optimize what is already fast enough.

### When a step fails

Never accumulate work on a broken foundation. Going back two steps is always cheaper
than debugging a cascade.

1. Stop.
2. Identify the last state that was correct.
3. Diagnose the root cause — not the symptom.
4. Replan the remaining steps from that state.
5. Resume with the corrected approach, not by retrying the same thing.

---

## 8. Close the loop

When the work is done, hand off to:

- **`project-memory`** — if a decision was made with tradeoffs, a constraint was
  discovered, or an approach failed for an instructive reason. Only durable, reusable
  knowledge. Not a transcript.
- **`postflight-audit`** — if the change carries real risk. Audit depth scales with
  that risk; a small change does not need a full review.

---

## Rules

1. Planning depth matches task complexity, in both directions.
2. Plans are internal by default.
3. **Default is zero agents.** Every agent needs a mission, bounded tools, and a
   stopping condition.
4. Search for existing implementations before writing new ones.
5. One question beats one wrong assumption — but only for critical ambiguity.
6. Validate the riskiest assumption before building, not after.
7. Follow the plan; if you are improvising, the planning was wasted.
8. A failed plan is information. Record it, do not just retry.
9. **Prefer the simplest implementation that meets the requirement.**
10. Meeting the success criteria is the signal to stop, not the signal to add more.
