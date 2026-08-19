---
name: deep-research
description: >
  Researches a question to a chosen depth with an explicit stopping criterion, ranking
  sources as primary, secondary, or unverified, triangulating the claims that matter, and
  separating evidence from interpretation. Use when asked to research, investigate, find
  out, verify, or fact-check something, when a claim needs sourcing before it is acted on,
  or on "investiga", "averigua", "qué se sabe de", "es cierto que", "busca fuentes",
  "how solid is this claim". Do NOT use for a single lookup that one search answers, for
  questions about this codebase, or for opinions where no evidence exists to find.
---

# Deep research

Two failures, opposite and equally common: stopping at the first plausible answer, and
reading thirty sources for a question that needed two.

The fix for both is deciding the depth **before** starting, and knowing what would make
you stop.

---

## 1. Pick a depth, and its stopping criterion

| Depth | Use when | Stop when |
|---|---|---|
| **QUICK** | A fact with a canonical home — a version number, a date, an API signature | The canonical source says it. One source is enough if it is *the* source. |
| **STANDARD** | An ordinary question with a settled answer that still needs checking | Two or three independent sources agree and nothing credible dissents. |
| **DEEP** | The answer will drive a decision that is expensive to reverse | Every load-bearing claim is triangulated against a primary source, and each known dissent is either explained or recorded. |
| **FORENSIC** | Sources conflict, or the claim is contested, or methodology is the question | The conflicts are mapped and attributed to their causes: different definitions, different periods, different methods, or a real disagreement. |

**Say the depth out loud at the start.** "This is a QUICK one — checking the changelog."
It sets expectations and stops depth creep.

**Escalate only on evidence**, never on unease: sources contradict each other, the
canonical source turns out not to be canonical, or the answer changes the decision more
than expected. Escalating "to be safe" is how a two-source question becomes thirty.

## 2. Rank every source

| Tier | What it is | Weight |
|---|---|---|
| **PRIMARY** | The thing itself: official docs, the specification, the source code, the filing, the dataset, the paper |
| **SECONDARY** | Someone reporting on a primary: articles, blog posts, summaries, courses |
| **UNVERIFIED** | Claims with no traceable origin: forum posts, social media, undated pages, anything an AI produced |

**A secondary source that cites a primary is worth less than the primary it cites.** Go
to the primary. Most of the time it is one click away and says something slightly
different.

**Tag every claim with its tier as you collect it**, not afterwards. Retrofitting tiers
is how a forum post becomes "reportedly".

## 3. Triangulate what matters

Not everything. Triangulate the claims that **carry the conclusion** — the ones where
being wrong changes the answer.

Independence is the whole point: three articles quoting the same press release are one
source wearing three hats. Ask where each source got it.

## 4. Separate evidence from interpretation

Say what was found and what you make of it — as two different things.

> **Evidence:** The changelog for 4.2 lists the flag as deprecated; the migration guide
> does not mention it. (PRIMARY, both.)
> **Reading:** It is likely removed in 5.0, but that is inference — no source says so.

**Never let inference inherit the confidence of its evidence.** This is the single most
common way research misleads.

## 5. Report

- **Cite per claim**, not a bibliography at the end. A reader must see which source backs
  which sentence.
- **Name the uncertainty.** "I could not find X" is a finding. Omitting it is not.
- **Record the dissent** you found and set aside, and why you set it aside.
- **State where you stopped and why** — the stopping criterion, met or abandoned.

---

## Rules

1. Depth first, then research. An unbounded search has no natural end.
2. One canonical source beats five that quote it.
3. Tag the tier as you collect, never after.
4. Triangulate what carries the conclusion; leave the rest.
5. Independent means independent origin, not different URLs.
6. Evidence and interpretation are two sections, never one sentence.
7. Cite per claim.
8. "Not found" is a result. Report it.
9. Escalate depth on evidence, never on unease.
