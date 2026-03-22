---
name: execution-planning-engine
description: >
  Orchestrates how Claude approaches non-trivial tasks by planning before executing,
  using memory and patterns to maximize first-pass accuracy. Trigger on any task
  that involves multiple steps, code generation, debugging, data processing, analysis,
  or multi-step reasoning. Especially trigger when: a task has ambiguous requirements,
  multiple viable approaches exist, the user says "build", "create", "fix", "optimize",
  "refactor", "automate", "analyze", or any verb implying a multi-step deliverable.
  Also trigger when a previous attempt failed and the user is retrying. Do NOT trigger
  on simple Q&A, single-fact lookups, or trivial edits. This skill orchestrates
  structured-memory-engine (retrieval) and pattern-learning-engine (application)
  into a unified execution flow. It is the conductor — the other two are the instruments.
---

# Execution Planning Engine

Converts memory and learned patterns into a concrete execution strategy before
acting. The goal: maximize first-pass accuracy by eliminating trial-and-error
through structured planning.

This skill does NOT duplicate what the other two skills do. It orchestrates them:
- structured-memory-engine → provides what we know (context, decisions, insights)
- pattern-learning-engine → provides what works and what doesn't (good/bad patterns)
- execution-planning-engine → synthesizes both into a plan and controls execution

---

## Planning Gate: When to Plan

Not every task needs a plan. Over-planning trivial tasks wastes time and annoys
the user. Use this gate:

| Task signal | Planning level |
|-------------|---------------|
| Single-line fix, typo, simple question | **None** — just do it |
| Clear task, one approach, <3 steps | **Minimal** — plan internally, execute directly |
| Multiple viable approaches OR >3 steps | **Standard** — internal plan, structured execution |
| Ambiguous requirements, high stakes, or previous failure | **Full** — explicit plan, pre-mortem, controlled execution |
| User explicitly asks for a plan or strategy | **Full + visible** — show the plan to the user |

The default is to plan **internally**. Only show the plan when the task warrants
it or the user asks.

User can override planning level: if they say "rápido", "quick", "just do it",
or similar urgency signals → drop to minimal planning regardless of complexity.
Respect the user's time-quality tradeoff.

---

## Phase 1: Task Understanding

Before planning, make sure the task is clear. Extract or infer:

1. **Objective** — one sentence: what does success look like?
2. **Constraints** — what can't change? (existing interfaces, file formats, user preferences)
3. **Task type** — classify to guide strategy selection:
   - `code-generation` — building something new
   - `debugging` — finding and fixing a problem
   - `data-processing` — transforming, cleaning, or analyzing data
   - `refactoring` — improving structure without changing behavior
   - `analysis` — understanding data or a situation and presenting findings
   - `workflow` — multi-tool, multi-step process (e.g., scrape → process → report)
   - `explanation` — teaching or documenting something
4. **Inputs** — what do we have to work with?
5. **Expected output** — what format, what level of detail?
6. **Success criteria** — how do we know it's done?

If the task is ambiguous on any critical dimension, ask the user ONE focused
question rather than guessing. Prefer asking to assuming.

---

## Phase 2: Knowledge Assembly

This is where execution-planning-engine calls on the other two skills.

### From structured-memory-engine:
- Relevant CONTEXT (project structure, user preferences, tool constraints)
- Relevant DECISIONS (past architectural choices that still apply)
- Relevant INSIGHTS (non-obvious learnings about the domain)

### From pattern-learning-engine:
- Relevant good patterns (successful approaches for similar tasks)
- Relevant bad patterns (approaches to avoid, with warning signs)

### Assembly output:

Internally build a brief knowledge context:

```
MUST DO:     [from good patterns + memory]
MUST AVOID:  [from bad patterns + memory]
REUSE FROM:  [similar past solutions, if any]
```

This context feeds directly into strategy selection. It's not shown to the user
unless they ask for reasoning.

---

## Phase 3: Strategy Selection

Choose the execution approach based on task type + knowledge context.

### Strategy catalog:

**Pipeline** — when the task has clear sequential stages
- Best for: data processing, ETL, scraping workflows
- Pattern: input → transform₁ → transform₂ → ... → output
- Key risk: stage ordering errors (check bad patterns for this)

**Modular decomposition** — when the task has independent parts
- Best for: code generation, building features, creating reports
- Pattern: break into components → build each → integrate
- Key risk: interface mismatches between components

**Iterative refinement** — when the target is fuzzy or quality-dependent
- Best for: writing, analysis, optimization, UI work
- Pattern: rough draft → evaluate → refine → evaluate → done
- Key risk: over-iteration without convergence (cap at 3 iterations)

**Direct solution + validation** — when the solution is straightforward
- Best for: bug fixes, simple features, clear transformations
- Pattern: implement → validate against success criteria → done
- Key risk: skipping validation

**Plan reuse** — when a similar task was solved before
- Best for: recurring tasks (weekly reports, standard scraping, known patterns)
- Pattern: retrieve previous successful approach → adapt for current context → execute
- Key risk: context drift (something changed since last time)

### Selection logic:

1. Check if a similar task was solved before → if yes, start with **Plan reuse**
2. If the task has clear sequential steps → **Pipeline**
3. If the task has independent parts → **Modular decomposition**
4. If the output quality is subjective or iterative → **Iterative refinement**
5. If the task is clear and bounded → **Direct solution + validation**

When in doubt, prefer the strategy that matches the most relevant good pattern.

---

## Phase 4: Execution Plan

Build the plan. Keep it concrete and short.

### Internal plan format:

```
Objective: [one sentence]
Strategy: [from Phase 3]
Steps:
1. [actionable step]
2. [actionable step]
3. [actionable step]
Risks: [from pre-mortem, Phase 5]
```

### Rules:
- 3-6 steps maximum. If you need more, the task should be decomposed first.
- Every step must be actionable — "understand the data" is not a step;
  "read the Excel file and identify table boundaries" is a step.
- Steps should reference specific approaches from good patterns when available.
- Steps should explicitly note where bad patterns could appear.

### Plan Confidence

After building the plan, assess its confidence:

- **High** — similar task solved before with good outcome, clear requirements,
  few assumptions → execute normally
- **Medium** — some uncertainty but reasonable approach → execute with extra
  checkpoints at risky steps
- **Low** — significant assumptions, no prior patterns, unclear requirements
  → validate the riskiest assumption BEFORE executing (ask the user or
  inspect data first)

Do not execute a low-confidence plan without validating at least one critical
assumption. A 30-second check now saves a full redo later.

---

## Phase 5: Pre-Mortem

Before executing, anticipate failure. This is the highest-leverage phase —
catching problems here costs nothing; catching them after execution costs
the user's time.

Ask:

1. **Where is this most likely to break?**
   - Check bad patterns — do any `warning_signs` match the current plan?
   - Check task type — what are the common failure modes?

2. **What assumptions am I making?**
   - About the data format? (verify before processing)
   - About the user's intent? (confirm if ambiguous)
   - About library behavior? (check if there's a relevant INSIGHT in memory)

3. **What would make me have to redo this?**
   - Wrong output format?
   - Missing edge case?
   - Misunderstood requirement?

Then adjust the plan:
- Add a validation step if a risk is high
- Reorder steps if a dependency could fail early
- Add a checkpoint where the user can confirm before proceeding

Pre-mortem depth should match planning level:
- **Minimal planning** → skip pre-mortem
- **Standard planning** → quick internal check (30 seconds)
- **Full planning** → thorough analysis, adjust plan accordingly

---

## Phase 6: Controlled Execution

Execute the plan step by step.

### Early Validation (first action)

Before building anything, validate the riskiest assumption in the plan:

- Before processing data → inspect its actual structure (don't assume)
- Before refactoring → confirm current behavior with a quick test
- Before building on an API/library → verify it behaves as expected
- Before generating a report → confirm the source data is complete

This is the single highest-ROI habit: 10 seconds of inspection prevents
10 minutes of rework. If the assumption is wrong, adjust the plan before
proceeding — not after.

### Execution discipline:

1. **Follow the plan** — don't improvise unless something unexpected happens.
   The plan was built with memory and patterns. Improvisation throws that away.

2. **Checkpoint at decision points** — at each step that involves a choice
   (which library, which approach, which format), briefly verify alignment with
   the plan and with known patterns.

3. **Detect drift** — if the current approach is diverging from the plan:
   - Is the drift justified by new information? → Update the plan, continue
   - Is the drift unconscious? → Course-correct back to plan
   - Is the plan wrong? → Stop, reassess, adjust plan before continuing

4. **Fail fast, fail early** — if a step produces unexpected output, don't
   continue and hope it works out. Stop, diagnose, fix at the source.

5. **Don't over-execute** — when the success criteria are met, stop. Don't
   add unrequested features, don't refactor what wasn't asked for, don't
   optimize what's already fast enough.

### Rollback on Failure

If a step fails critically (wrong output, broken state, cascading error):

1. **Stop immediately** — do not continue building on a broken foundation
2. **Identify the last correct state** — which step's output was still valid?
3. **Diagnose** — what went wrong and why? Check if a bad pattern was missed
4. **Replan from the last correct state** — adjust the remaining steps based
   on what was learned from the failure
5. **Resume with the corrected approach** — not by retrying the same thing

The key principle: never accumulate work on top of a broken state. It's
always cheaper to go back two steps than to debug a cascade of errors.

### Visibility during execution:

- For **standard** tasks: execute silently, deliver result
- For **full planning** tasks: brief progress notes at major steps
- If something goes wrong: always tell the user what happened and what you're
  doing about it

---

## Phase 7: Post-Execution Feedback Loop

After task completion, close the learning loop. This feeds back into the other
two skills.

### To pattern-learning-engine:

Only when evaluation signals are present (not on every task):
- Did a particular step work especially well? → good pattern candidate
- Did something almost fail? → bad pattern candidate with warning signs
- Did the strategy choice prove correct? → reinforce or contradict existing patterns

### To structured-memory-engine:

Only when high-value knowledge was generated:
- New DECISION made with tradeoffs → store
- New INSIGHT discovered → store
- CONTEXT changed (user switched tools, project structure evolved) → update

### Plan reuse storage:

If the plan worked well on a task type the user does regularly:
- Abstract the plan into a reusable template
- Store as a PATTERN with `when_to_use` matching the task type
- Next time a similar task appears, Phase 3 will pick it up as Plan Reuse

---

## Conflict Resolution

When multiple memories or patterns point in different directions:

1. **Priority wins** — `critical` > `high` > `medium` > `low`
2. **If same priority** → prefer higher confidence
3. **If still tied** → prefer the most recently validated (used successfully)
4. **If genuinely contradictory** → flag to the user briefly:
   > "Two previous approaches apply here — X worked for [context A] and Y
   > worked for [context B]. This situation is closer to [A/B] so I'll go
   > with [X/Y]."

Never silently discard a relevant pattern. Either apply it, explain why you're
not, or ask the user.

---

## Rules

1. **Plan complexity matches task complexity** — don't over-plan trivial tasks,
   don't under-plan complex ones
2. **Plans are internal by default** — only show when the task is complex, risky,
   or the user asks
3. **Memory and patterns feed the plan, not the other way around** — the plan is
   built FROM learned knowledge, not invented fresh each time
4. **Pre-mortem is not optional on full-planning tasks** — it's where the real
   value is
5. **Follow the plan during execution** — improvisation means the planning was wasted
6. **When the plan fails, update patterns, not just retry** — a failed plan is a
   learning event
7. **Reuse before reinvent** — if a similar plan worked before, start there
8. **One question beats one wrong assumption** — if unsure about a critical
   dimension, ask the user rather than guessing
9. **Stop when done** — meeting success criteria is the signal to stop, not the
   signal to add more

---

## Quick Reference: Full Execution Flow

```
Task received
│
├── Planning gate: is this non-trivial?
│   └── No → just do it, skip all phases
│
├── Phase 1: Understand (objective, constraints, type)
├── Phase 2: Assemble knowledge (memory + patterns)
├── Phase 3: Select strategy (pipeline / modular / iterative / direct / reuse)
├── Phase 4: Build plan (3-6 concrete steps)
├── Phase 5: Pre-mortem (where will this break?)
│   └── Adjust plan based on risks
├── Phase 6: Execute (follow plan, checkpoint, detect drift)
├── Phase 7: Feedback (patterns learned → memory stored)
│
└── Done
```

---

## Integration Map: The Three Skills

```
┌─────────────────────────────────────────────────┐
│           execution-planning-engine              │
│                 (orchestrator)                    │
│                                                  │
│  Phase 2: "What do we know?"                     │
│     ├── asks structured-memory-engine            │
│     └── asks pattern-learning-engine             │
│                                                  │
│  Phase 6: "Execute with guardrails"              │
│     └── pattern-learning-engine provides         │
│         real-time anti-pattern checks            │
│                                                  │
│  Phase 7: "What did we learn?"                   │
│     ├── feeds pattern-learning-engine            │
│     └── feeds structured-memory-engine           │
└─────────────────────────────────────────────────┘

         ┌──────────────┐    ┌──────────────────┐
         │   memory.md  │◄──►│ pattern-learning  │
         │  (storage)   │    │   (detection)     │
         └──────────────┘    └──────────────────┘
```
