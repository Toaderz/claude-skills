---
name: project-memory
description: >
  Reads and writes durable project knowledge in .claude/memory/ so decisions,
  constraints, and lessons survive across sessions instead of being re-derived. Use
  when starting substantive work on a codebase, after a decision with real tradeoffs,
  when a constraint is discovered or an approach fails instructively, when the user
  corrects an approach, when asked what was decided before or why something is the way
  it is, or on "remember this", "next time", "always", "never", "recuerda esto", "la
  próxima vez", "no vuelvas a". Do NOT use to log transcripts, record temporary state,
  restate obvious facts, or store anything that will not change a future decision.
---

# Project memory

Durable knowledge about *this* project, in files, in the project. Not a transcript,
not a diary, not a second copy of the codebase.

The test for every entry:

> Will this change a decision someone makes later?

If no, it does not go in.

---

## Where it lives

```
.claude/memory/
├── MEMORY.md      # project facts: structure, conventions, environment, preferences
├── decisions.md   # choices made, with the reasoning and the tradeoff
└── lessons.md     # what failed and why, with the signs that predict it
```

These are plain markdown, in the project being worked on, created on first write with
`Write` and updated with `Edit`. They are read with `Read`. There is no special tool
and no external store — if a mechanism is not one of the ordinary file tools, it does
not exist and must not be relied on.

Commit them or gitignore them, per the project's convention. Ask once, record the
answer in `MEMORY.md`, do not ask again.

---

## Reading

**At the start of substantive work, read `.claude/memory/` if it exists.** Not for
trivial tasks — reading three files to fix a typo is the cost this skill is supposed
to avoid.

Then:

- **Apply what is relevant, silently.** Weave it into the approach. Do not present a
  list of retrieved memories.
- **Mention it only when it changes the approach**, and then in one clause:
  "Renaming after the scrape — doing it first broke title-matching last time."
- **Say nothing when nothing applies.** "No relevant memory found" is noise.

If the directory does not exist, proceed normally. Create it on the first entry that
passes the filter below, not preemptively.

---

## Writing

### The filter — all four must hold

1. **Reusable.** Applies beyond this one file, row, or run.
2. **Project-specific.** General programming knowledge does not belong here.
3. **Non-obvious.** If any competent person would already know it, skip it.
4. **Decision-changing.** It will alter what someone does later.

Fails any one → do not write it.

### What goes where

| File | Content | Example |
|---|---|---|
| `MEMORY.md` | stable facts: layout, conventions, environment quirks, user preferences, how to run things | "Tests run with `pytest -m 'not slow'`; the slow marker needs a live DB." |
| `decisions.md` | a choice, its alternatives, and why | "Chose openpyxl over pandas: the sheets are not tabular and pandas assumes a header row." |
| `lessons.md` | a failure, its root cause, and its warning sign | "Renaming columns before the scrape breaks title matching — the scraper uses original names as lookup keys. Warning sign: mutating shared state before its consumers are done." |

### Format

Keep entries short and self-contained. One heading, two to four lines.

```markdown
## Column renames happen after the scrape, never before
The scraper uses original column names as lookup keys, so renaming first breaks
title matching. Root cause: mutating shared state before its consumers finish.
Warning sign: any transform that touches a field another step still reads.
```

Rules that keep entries useful:

- **Abstract before writing.** "Rename derived fields after the scrape completes,"
  not "rename column B to Ticker after line 47 of ft_scraper.py."
- **Root cause, not symptom.** "The column names were wrong" teaches nothing.
- **Include the warning sign** for lessons. A lesson you cannot recognize in advance
  cannot prevent anything.
- **Date nothing.** Entries that stop being true get deleted, not annotated as stale.

### When to write

| Trigger | Goes to |
|---|---|
| A choice was made between real alternatives | `decisions.md` |
| A constraint was discovered the hard way | `MEMORY.md` |
| An approach failed for an instructive reason | `lessons.md` |
| The user corrected the approach | `lessons.md` |
| The user stated a preference or convention | `MEMORY.md` |
| A tool or library behaved unexpectedly | `lessons.md` |
| The user said "remember", "always", "never", "next time" | whichever fits |

Write silently. Do not announce every write.

---

## Updating and deleting

Memory that only grows stops being useful. Both of these are part of the job:

- **Update** an entry when reality changes. Rewrite it in place; do not add a second
  entry that contradicts the first.
- **Delete** an entry when it is wrong, superseded, or about a part of the project
  that no longer exists. Deleting a stale entry is a contribution, not a loss.

When a new entry overlaps an existing one, **merge** them. Two entries about the same
thing means neither will be trusted.

---

## Compaction

Compact by **judgment, not by count.** There is no "every 25 entries" rule, because
entry count is not what makes memory expensive.

Compact when:

- **Size** — a file has grown past roughly 200 lines and is loaded often.
- **Redundancy** — several entries circle the same underlying fact.
- **Age** — entries describe code, tools, or workflows that no longer exist.
- **Low information value** — an entry has never once changed a decision.

How:

1. Merge overlapping entries into the strongest single statement.
2. Delete entries invalidated by the current state of the project.
3. Promote what recurs — a lesson hit three times is a convention; move it to
   `MEMORY.md` as a rule.
4. Cut anything that has never been used and no longer looks likely to be.

**The point of memory is to reduce repeated context. A memory file that costs more
to load than the knowledge saves is a net loss** — compact it or delete it.

---

## Conflicts

When memory contradicts your default approach:

1. Memory carries real weight — it is learned experience in this specific project.
2. If it clearly applies, follow it.
3. If the context has genuinely changed, say so in one line and proceed:
   "Memory says X, but this path uses Y instead, so going with Z."
4. If unsure, ask rather than silently ignoring it.

**When memory is overridden for good reason, annotate it rather than deleting it** —
the exception makes the entry sharper.

If the user corrects a mistake that an existing entry was supposed to prevent, that
entry failed at being findable. Rewrite it so it is unmissable next time: sharper
title, more specific trigger.

---

## What never goes in

- Conversation transcripts or summaries of what was discussed
- Temporary state: what is half-done, what is being worked on right now
- Facts recoverable by reading the code
- General programming knowledge
- Anything already recorded, in different words
- Anything that has stopped being true

---

## Rules

1. Ten sharp entries beat a hundred mediocre ones.
2. Abstract before writing; store the principle, not the instance.
3. Root cause, never symptom.
4. Every lesson carries its warning sign.
5. Merge on overlap, never duplicate.
6. Delete what is stale — pruning is maintenance, not loss.
7. Retrieval is routine; verbalizing it is selective.
8. Write silently.
9. **Memory must cost less than the context it saves.**
