---
name: decision-comparison
description: >
  Compares options against criteria stated before the verdict, surfaces the trade-off each
  one actually carries, names what is still unknown, and only then recommends — or says
  plainly that it cannot yet. Use when asked which of several options to pick, to compare
  alternatives, to weigh a tradeoff, to help decide between approaches, tools, libraries,
  vendors, or designs, and on "cuál conviene", "cuál me recomiendas", "compara", "vale la
  pena", "which should I use", "is X better than Y", "pros and cons". Do NOT use when only
  one option exists, when the choice is already made and only execution remains, or for a
  factual lookup with no decision attached.
---

# Decision comparison

A recommendation is only as good as the criteria it was measured against. State them
first, or the comparison is a rationalisation of a choice already made.

This applies to anything with options and a decision: libraries, architectures, vendors,
designs, hiring, hotels. **The shape of the question is what matters, not the domain.**

---

## 1. Options

List what is actually being compared, including the ones not proposed:

- **Do nothing / keep the current thing.** Almost always a real option, almost never
  listed. If it loses, say why — that is half the argument for changing.
- **The obvious option nobody mentioned**, if there is one.
- Drop options that fail a hard constraint, and **say you dropped them and why**. A
  silently omitted option looks like an oversight.

Three to five is usually right. Two is often a false binary; eight is a list, not a
comparison.

## 2. Criteria — before any verdict

Name the criteria and **weight them**, because they are never equal. Get them from the
actual situation, not from a generic list.

> "Weighting: migration cost heavily — this has to ship in two weeks. Performance barely
> — the dataset is 4,000 rows and will stay that size."

**If the criteria come out after the recommendation, the comparison is theatre.** The
weights are where the real decision is made, and they are the part the user is best
placed to correct.

## 3. Evidence

Fill the comparison with what is true, marking how you know:

| | Verified | Reported | Assumed |
|---|---|---|---|
| Meaning | you ran, read, or tested it | a source says so | you are inferring |

**Never present an assumption in the same voice as a measurement.** A table where every
cell reads with equal authority is more misleading than no table.

Where a cell is empty, leave it empty. An invented value is worse than a gap.

## 4. Trade-offs

For each surviving option, state what you actually give up by choosing it. An option with
no stated cost has not been examined.

> "Postgres: gives up the zero-setup local story. Every contributor now needs a running
> instance, or the test suite needs a substitute."

**Beware the option that wins on every criterion.** Either a criterion is missing, or the
comparison was built to reach that answer.

## 5. Unknown / missing data

A required section, not an optional caveat. What would change the answer, and what you
could not establish:

> "Unknown: whether the managed tier includes the extension. That is the whole cost
> argument for option B — if it does not, B is not viable."

## 6. Recommend — or decline to

Give a clear recommendation, tied to the weights from step 2, with the condition that
would flip it:

> "Option A, because migration cost dominates and A needs no schema change. If the
> two-week deadline moves, B becomes better within a quarter."

**"I cannot recommend yet, because X is unknown" is a valid and often correct output.**
Say what X is, what would resolve it, and how long that takes. A confident recommendation
resting on an unknown is the failure this skill exists to prevent.

Never end on a menu. If the user must choose, tell them which fact decides it.

---

## Rules

1. Criteria and weights before the verdict. Always in that order.
2. "Keep what we have" is an option. List it.
3. Mark verified, reported, and assumed differently.
4. Empty beats invented.
5. Every option states what it costs.
6. An option that wins on everything means a criterion is missing.
7. Unknown / missing data is a required section.
8. "Not yet" is a valid recommendation; a menu is not.
9. Name the condition that would flip the answer.
