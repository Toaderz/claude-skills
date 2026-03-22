---
name: pattern-learning-engine
description: >
  Continuously improves Claude's performance by detecting good and bad patterns
  from task outputs and feeding them into structured-memory-engine for storage.
  Trigger on EVERY task where output quality matters — coding, analysis, writing,
  debugging, data processing, problem solving, or any iterative work. Especially
  trigger when: Claude produces a response and the user reacts (positively or
  negatively), a task requires multiple attempts, Claude catches its own mistake,
  the user says "that's wrong", "perfect", "not what I meant", "do it like before",
  "why did you do X", or any feedback that implies a quality judgment. Also trigger
  after completing multi-step tasks to extract what worked across the full sequence.
  This skill detects patterns; structured-memory-engine stores them. They work as
  a pair — detection feeds storage, storage feeds future detection.
---

# Pattern Learning Engine

Detects reusable good and bad patterns from Claude's own outputs. Operates as the
analytical layer that feeds into structured-memory-engine for persistence. The goal
is not to evaluate everything — it's to catch the patterns that actually change
future performance.

---

## Core Principle: Selective Evaluation

Do NOT run a full self-evaluation after every single response. That creates noise.
Instead, evaluate when evaluation signals are present:

| Signal | Evaluation depth |
|--------|-----------------|
| User says "perfect", "great", "exactly" | Light — tag what worked |
| User corrects or rejects output | Deep — root cause analysis |
| Task took 3+ iterations to get right | Deep — extract the winning approach |
| Claude catches own mistake mid-task | Medium — capture the self-correction |
| Complex task completed successfully | Medium — extract structural patterns |
| Simple Q&A or factual response | None — skip evaluation entirely |
| User gives no feedback | None — don't assume quality |

---

## Phase 1: Pattern Detection

When an evaluation signal fires, analyze the output along these dimensions:

### For Good Patterns (what worked)

Identify the specific technique, not vague praise:

```
BAD detection:  "The response was well-structured"
GOOD detection: "Breaking the Excel parser into scan → detect → parse → build
                 pipeline stages prevented the monolithic function problem
                 that caused bugs in the previous approach"
```

Ask:
- What specific technique or structure made this work?
- Would this work again on a similar task?
- What's the minimum abstraction that captures the technique?

### For Bad Patterns (what failed)

Always trace to root cause, not symptoms:

```
BAD detection:  "The column names were wrong"
GOOD detection: "Renaming columns before scraping broke title-matching because
                 the scraper uses original column names as lookup keys.
                 Root cause: modifying shared state before consumers are done
                 with the original values"
```

Ask:
- What was the root cause, not the visible symptom?
- At what point in the process did things go wrong?
- What decision led to this failure?

---

## Phase 2: Pattern Formatting

Convert detected patterns into structured entries ready for memory storage.

### Good Pattern Entry

```json
{
  "type": "PATTERN",
  "polarity": "good",
  "priority": "critical | high | medium | low",
  "title": "Short imperative name (e.g., 'Pipeline decomposition for parsers')",
  "technique": "The specific approach that worked",
  "why_it_works": "Causal explanation — not just 'it was better'",
  "when_to_use": "Concrete trigger conditions for reuse",
  "abstraction": "Generalized version that applies beyond this specific task"
}
```

### Bad Pattern Entry

```json
{
  "type": "PATTERN",
  "polarity": "bad",
  "priority": "critical | high | medium | low",
  "title": "Short descriptive name (e.g., 'Mutating shared state before consumers finish')",
  "what_happened": "The concrete failure",
  "root_cause": "Why it failed at the deepest level",
  "what_to_do_instead": "The correct approach",
  "warning_signs": "How to recognize this situation before making the mistake"
}
```

---

## Phase 3: Generalization Filter

Before sending a pattern to memory, generalize it. The goal is to make patterns
portable across different tasks and projects.

### Generalization rules:

1. **Remove proper nouns** — "rename FT Portfolios columns post-scrape" becomes
   "rename derived fields after scraping completes, not before"

2. **Extract the principle** — "use openpyxl instead of pandas for PRESUPUESTO file"
   becomes "use cell-level access libraries when spreadsheet structure is unpredictable"

3. **Identify the category** — tag patterns by domain:
   - `code-architecture` — how to structure code
   - `data-pipeline` — ordering of operations, data flow
   - `tool-usage` — library/tool selection and configuration
   - `debugging` — diagnostic approaches
   - `communication` — how to present results to the user
   - `workflow` — process and sequencing of steps

4. **Test portability** — ask: "Would this help on a task in a completely different
   project?" If yes, the abstraction level is right. If no, generalize more.

---

## Phase 4: Memory Handoff

This is where pattern-learning-engine connects to structured-memory-engine.

### Within session:

Write the formatted pattern entry to the session memory file:
`/home/claude/Claude_optimization/session_memory.json`

Use the exact schema defined in structured-memory-engine's SKILL.md:

```json
{
  "id": "<next_id>",
  "type": "PATTERN",
  "title": "<from pattern entry>",
  "content": "<technique or what_happened + root_cause>",
  "why_it_matters": "<why_it_works or what_to_do_instead>",
  "when_to_use": "<trigger conditions>",
  "source_task": "<brief task description>",
  "confidence": "high | medium | low",
  "priority": "critical | high | medium | low",
  "promote_to_persistent": false
}
```

### Promotion recommendation:

Mark `promote_to_persistent: true` when the pattern meets ANY of:
- User explicitly confirmed the pattern ("yes, always do it that way")
- Same pattern detected twice in one session
- Pattern corrects a mistake Claude made more than once
- Pattern applies to the user's core workflows (weekly reports, scraping, Excel parsing)

Structured-memory-engine handles the actual promotion to persistent memory.

---

## Phase 5: Pattern Application (MANDATORY)

Pattern application happens at two moments: before the task and during execution.

### 5A: Pre-Task Retrieval (before starting)

Before starting any task that could match stored patterns:

1. **Retrieve** applicable patterns from session memory and persistent memory
2. **Rank** by priority: `critical` → `high` → `medium` → `low`
3. **Select** top 1-3 most relevant patterns
4. **Apply** them in the approach

Visibility rules — surface a pattern to the user ONLY when:
- Avoiding a known bad pattern that the user previously hit
- The pattern materially changes the approach (not just a minor optimization)
- The user previously complained about the exact issue the pattern addresses

Otherwise, apply silently. The user should experience better quality, not a
narration of the machinery.

### 5B: Real-Time Pattern Guidance (during execution)

Patterns are not only retrospective — they also guide execution in real time.

During multi-step tasks, run a lightweight checkpoint at natural decision points
(choosing a library, structuring code, deciding on an approach):

1. Does the current approach align with known good patterns? → Continue
2. Is the current approach drifting toward a known bad pattern? → Course-correct

Course correction protocol:
- If a bad pattern's `warning_signs` match the current situation:
  - Stop the current approach before completing it
  - Switch to the alternative from `what_to_do_instead`
  - Briefly mention the course correction if it changes the user-visible approach
  - Example: "I was about to rename columns first, but that breaks downstream
    matching — doing it post-scrape instead."

This is NOT constant monitoring of every line of output. It's a checkpoint at
key decision moments — typically 2-4 times per complex task.

### 5C: Anti-Pattern Enforcement

Bad patterns with `critical` or `high` priority act as strong guardrails:

1. If approaching a known bad pattern → switch to the stored alternative
2. If no stored alternative exists → flag the risk and propose a different approach
3. If the context genuinely makes the "bad" pattern the right choice → explain
   why this is an exception and proceed, but annotate the pattern with the
   exception case for future reference

Bad patterns are strong warnings, not absolute blocks. Context can override them,
but the override must be conscious and justified, never silent.

---

## Phase 6: Pattern Lifecycle

Patterns aren't permanent. They evolve:

### Strengthen
When a pattern proves useful again → increase confidence, add the new context
to its `when_to_use` field.

### Merge
When two patterns describe the same underlying principle → combine into one
stronger entry with broader applicability.

### Retire
When a pattern no longer applies (user changed tools, project ended, approach
was superseded) → mark for removal in next memory evolution cycle.

### Contradict
When a new observation contradicts a stored pattern → don't silently delete.
Instead, flag the conflict:
> "Previous pattern suggested X, but this result shows Y works better in
> this context. Updating the pattern."

---

## Interaction Rules

1. **Detection is always on, output is selective** — constantly observe, rarely narrate
2. **Never say "this was good" without saying WHY** — vague praise is noise
3. **Root cause or nothing** — surface-level failure descriptions don't prevent recurrence
4. **One good pattern is worth ten observations** — be selective, not exhaustive
5. **Patterns must be actionable** — "be more careful" is not a pattern;
   "validate DataFrame shape after merge to catch silent row drops" is a pattern
6. **Don't evaluate trivial interactions** — "what time is it?" needs no pattern analysis
7. **Respect structured-memory-engine's filters** — this skill detects, that skill decides
   what to keep
8. **Priority drives behavior** — `critical` patterns are near-mandatory to follow;
   `low` patterns are applied only on clear match
9. **Bad patterns are proactive, not reactive** — catch them BEFORE they cause damage,
   not after

---

## Quick Reference: Evaluation Decision Tree

```
Output produced
├── User gave explicit feedback?
│   ├── Positive → Light eval: tag technique that worked
│   └── Negative → Deep eval: root cause analysis
├── Multiple iterations needed?
│   └── Yes → Deep eval: compare approaches, extract winner
├── Claude self-corrected?
│   └── Yes → Medium eval: capture the correction pattern
├── Complex multi-step task completed?
│   └── Yes → Medium eval: extract structural patterns
└── None of the above?
    └── Skip evaluation — no signal, no eval
```
