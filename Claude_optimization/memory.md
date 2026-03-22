---
name: structured-memory-engine
description: >
  Captures high-value patterns, decisions, insights, and context from every interaction
  and stores them for future use. Trigger this skill on EVERY conversation — it runs
  passively in the background. Especially trigger when: the user completes a task and
  something worked well or failed, the user corrects Claude's approach, a non-obvious
  solution is discovered, a workflow preference is expressed, a decision is made with
  tradeoffs, the user says "remember this", "don't do that again", "this worked",
  "next time do X", or any phrase implying a reusable lesson. Also trigger when
  starting a new task to check if stored memory applies. Works alongside
  pattern-learning-engine for cumulative intelligence across sessions.
---

# Structured Memory Engine

Captures only high-value knowledge from interactions and makes it available for future
use. Operates through two storage layers: session memory (rich, temporary) and
persistent memory (distilled, survives across conversations).

---

## Storage Architecture

### Layer 1: Session Memory (within conversation)

File: `/home/claude/Claude_optimization/session_memory.json`

This file is created at the start of each conversation and accumulates detailed
entries throughout. It resets between sessions, so it holds the raw, rich version
of everything learned during the current interaction.

Schema:

```json
{
  "session_date": "YYYY-MM-DD",
  "entries": [
    {
      "id": 1,
      "type": "PATTERN | CONTEXT | DECISION | INSIGHT",
      "title": "Short descriptive title",
      "content": "What was learned",
      "why_it_matters": "How this improves future work",
      "when_to_use": "Trigger condition for retrieval",
      "source_task": "Brief description of the task that produced this",
      "confidence": "high | medium | low",
      "priority": "critical | high | medium | low",
      "promote_to_persistent": false
    }
  ]
}
```

### Layer 2: Persistent Memory (across conversations)

Uses the `memory_user_edits` tool — the only mechanism that survives between sessions.
Limited to 30 entries of ~500 chars each. This is where the most distilled, highest-value
learnings get promoted.

Format for persistent entries (one per line in memory_user_edits):

```
[TYPE:PRIORITY] title :: condensed insight :: trigger condition
```

Examples:
```
[PATTERN:HIGH] Excel column rename must happen post-scrape :: renaming before scraping breaks title-matching in FT Portfolios scripts :: when editing scraping pipeline column names
[DECISION:MEDIUM] Use openpyxl over pandas for unstructured Excel :: pandas assumes tabular structure, openpyxl handles arbitrary cell layouts :: when parsing messy/unstructured Excel files
[INSIGHT:HIGH] BFS island detection outperforms grid-scan for sparse sheets :: fewer false positives on sheets with scattered data blocks :: when building table detection for sparse spreadsheets
```

---

## Memory Types

### 1. PATTERN
What works and what doesn't. Reusable approaches.
- Good patterns: techniques that produced correct results
- Bad patterns: approaches that caused bugs, regressions, or wasted time
- Source: direct observation or from pattern-learning-engine

### 2. CONTEXT
Key facts about the user, their projects, environment, and preferences.
- Project structures, naming conventions, file locations
- Tool preferences (Morningstar Direct, specific Python libraries)
- Workflow requirements (Monday reports, specific Excel formats)

### 3. DECISION
Important choices made and their rationale.
- Architecture decisions (why X over Y)
- Tradeoff analysis that was done
- Constraints that drove the decision

### 4. INSIGHT
Non-obvious learnings that improve reasoning.
- Surprising behaviors of tools or libraries
- Edge cases that aren't documented
- Meta-observations about what makes tasks succeed or fail

---

## Operating Protocol

### On Every Task Start (MANDATORY)

Retrieval is not optional. Execute these steps on every task, no exceptions:

1. Read `/home/claude/Claude_optimization/session_memory.json` if it exists
2. Check persistent memory (already in context via userMemories)
3. Select relevant entries (prioritize `critical` and `high` priority first, max 3-5)
4. **If relevant memory is found** → apply it naturally in the approach. Mention it
   only when it meaningfully changes the strategy:
   - Example: "I'll rename columns after the scrape completes — early renaming
     broke title-matching before."
   - Do NOT list memory items formally. Weave them into the response.
5. **If no relevant memory is found** → proceed normally, say nothing about memory.
   (Saying "no memory found" on trivial tasks adds noise.)

The key: always retrieve, selectively verbalize.

### Memory Compliance Rule

If relevant memory exists but Claude fails to apply it, and the user corrects
the same mistake that memory was meant to prevent:

1. This is a high-priority learning event
2. Strengthen the ignored memory entry — make its `when_to_use` more specific
   to match the exact situation where it was missed
3. Elevate its priority to `critical`
4. If it was only in session memory, promote it to persistent immediately

The goal: every time memory is ignored and the user pays the cost, the memory
becomes harder to ignore next time.

### Memory vs Default Reasoning

When a stored memory conflicts with Claude's default approach:

1. **Memory has strong influence but not absolute override** — memory represents
   learned experience from this specific user's context
2. If the memory clearly applies to the current situation → follow the memory
3. If the context has changed (different tools, different project, different
   constraints) → flag the conflict briefly:
   > "Previous experience says X, but this situation differs because Y.
   > Going with Z instead."
4. If unsure → ask the user rather than silently ignoring the memory

Memory that gets overridden with good reason doesn't get deleted — it gets
annotated with the exception case, making it smarter for next time.

### During Task Execution

Capture memory entries when ANY of these triggers fire:

| Trigger | Action |
|---------|--------|
| User corrects Claude's approach | Store as PATTERN (bad → good) |
| A non-obvious solution works | Store as INSIGHT |
| User expresses preference | Store as CONTEXT |
| A decision is made with tradeoffs | Store as DECISION |
| Something fails unexpectedly | Store as PATTERN (bad) |
| User says "remember", "next time", "always", "never" | Store matching type |
| A workaround is needed for a tool/library limitation | Store as INSIGHT |
| Task succeeds after multiple approaches | Store winning approach as PATTERN |

Write entries to session_memory.json silently — do not announce every write unless
the user asks about memory activity.

### Quality Filter (before storing)

Ask internally before each entry:

1. **Is this reusable?** → If it only applies to this exact file/row/cell, don't store
2. **Is this non-obvious?** → If anyone would know this, don't store
3. **Does this improve future performance?** → If not, don't store

If all three are NO → skip. If any is YES → store.

### On Task Completion

At natural conversation endpoints (task done, user satisfied, switching topics):

1. Review session memory accumulated so far
2. Identify entries worth promoting to persistent memory
3. Promotion criteria (must meet at least 2):
   - High confidence
   - Likely to recur in future tasks
   - Would save significant time if remembered
   - Corrects a mistake Claude is likely to repeat
4. Use `memory_user_edits` tool to add promoted entries
5. Before adding, check existing persistent memory for duplicates or conflicts
6. If an existing entry is outdated, replace it rather than adding a new one

### Memory Evolution (periodic)

When persistent memory approaches 25+ entries:

1. Review all entries for continued relevance
2. Merge entries that overlap (e.g., two PATTERN entries about the same topic)
3. Remove entries that haven't been useful (user never works on that topic anymore)
4. Prioritize entries that have been actively used in recent sessions

---

## Integration with pattern-learning-engine

When pattern-learning-engine is active:

- Patterns detected by that skill feed directly into this skill's PATTERN type
- This skill handles storage; pattern-learning-engine handles detection
- Avoid duplicate storage — if pattern-learning-engine already captured it,
  don't re-store here unless adding new context

When pattern-learning-engine is NOT active:

- This skill does basic pattern detection on its own using the trigger table above
- Less sophisticated than the dedicated engine but still captures the obvious wins

---

## Rules

1. **Selectivity over completeness** — 10 great entries beat 100 mediocre ones
2. **Abstract before storing** — "rename columns post-scrape" not "rename column B to 'Ticker' after running ft_scraper.py line 47"
3. **No redundancy** — check before adding; merge if similar exists
4. **Persistent memory is premium real estate** — only 30 slots, guard them carefully
5. **Silent operation** — don't narrate memory operations unless asked
6. **Session memory is disposable** — don't hesitate to write freely there; the promotion filter protects persistent memory
7. **When in doubt, store in session** — it costs nothing and gets filtered later
8. **Priority drives retrieval** — `critical` and `high` entries are always retrieved when relevant; `medium` entries are retrieved when the task domain matches; `low` entries are retrieved only on exact trigger match
9. **Retrieval is mandatory, verbalization is selective** — always check memory; only mention it when it changes the approach

---

## Quick Reference: Promotion Decision

```
Session entry candidate for promotion:
├── Used more than once this session? → Strong promote signal
├── User explicitly said "remember this"? → Promote immediately
├── Corrects a recurring Claude mistake? → Promote immediately
├── Specific to one file/task? → Do NOT promote
├── Already covered by existing persistent entry? → Do NOT promote (or merge)
└── Would help in a different project? → Promote
```
