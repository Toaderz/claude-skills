---
name: news-prioritization
description: >
  Ranks macro-financial news by macro impact, surprise, and direct relevance to a tracked
  investment universe, producing a scored shortlist with one actionable insight each. Use
  when asked to review, filter, rank, prioritise, or summarise recent market or macro
  news, when headlines are pasted and the question is which ones matter, or on "weekly
  news", "what matters this week", "macro recap", "news for my portfolio", "qué pasó en
  los mercados", "noticias de la semana", "qué me afecta del portafolio". Do NOT use for
  general or non-financial news, for a single company lookup, or for building a portfolio
  — this scores news against an existing universe, it does not pick assets.
---

# News Prioritization Skill

## Objective

Identify, evaluate, and rank the most relevant macro-financial news from the
last 7 days for the tracked investment universe. Output a clean, ranked list
with scores, ratings, signal strength, and one actionable insight per item.

---

## Step 0 — Load the investment universe

Read the universe from the **project**, in this order:

1. `.claude/investment_universe.md`
2. `investment_universe.md` at the project root
3. Whatever path the user names

**The universe is not bundled with this skill.** It is personal holdings; a plugin other
people install has no business carrying it. What ships here is the format contract:
[references/investment_universe.example.md](references/investment_universe.example.md).

The structure is the contract:

- Each `##` heading is a **sector** (`US`, `Tech`, `Japan`, `China`, …).
- Each bullet under a heading is an **exact asset name** — match these literally.
- An asset appearing under more than one heading takes the most specific sector.

**If no universe file is found, say so before scoring anything:**

> "No encuentro el investment universe en `.claude/investment_universe.md`, así que la
> relevancia de portafolio (0–5) no la puedo calcular. Puedo rankear solo por impacto
> macro (0–25), o me pasas el archivo."

Then either proceed with the core score alone and **mark every Portfolio Relevance cell
`n/a`**, or wait for the file. **Never invent a universe, and never silently score
Portfolio Relevance without one** — a fabricated 5 is worse than a stated gap.

---

## Step 1 — Deduplicate & Consolidate

Before scoring, group news items that cover the **same underlying event**
(e.g., three Fed-related headlines → one consolidated entry).

Rules:
- Same event + same day = merge into one entry, list all sources
- Same theme + different day = keep separate, note the sequence
- Keep the most informative headline as the primary title

---

## Step 2 — Score Each News Item

Score each consolidated news item across **6 dimensions**:

### A. Core Scoring (0–25)

| Dimension | 0 | 3 | 5 |
|-----------|---|---|---|
| **1. Macro Impact** | Local/micro event | Regional relevance | Global macro shift |
| **2. Surprise Factor** | Fully priced in | Partial surprise | Significant deviation from consensus |
| **3. Market Relevance** | No market reaction | Some reaction | Strong cross-asset reaction |
| **4. Forward Implications** | No change to outlook | Minor revision | Changes base case |
| **5. Structural vs Noise** | Pure noise/one-off | Mixed signal | Structural regime change |

Each dimension: 0–5 points → **Max: 25**

### B. Portfolio Relevance (0–5)

Match the news against the universe loaded in Step 0:

| Score | Criteria |
|-------|----------|
| **5** | Direct impact on a specific named asset (exact match) |
| **4** | Strong sector impact affecting multiple assets in universe |
| **3** | Macro/thematic impact affecting broad universe exposure |
| **2** | Weak indirect relevance |
| **1** | Very distant relation |
| **0** | No relevance to the investment universe |

**Matching rules:**
- Match asset names literally against the bullets under any sector heading
- Match ETFs by their stated exposure (e.g., CIBR → cybersecurity news)
- Match sectors using the `##` headings themselves
- If an asset appears in multiple sectors, use the most specific match
- If news impacts S&P 500, MSCI ACWI, or NASDAQ → treat as broad universe exposure (score 3 minimum)

### C. Time Decay Adjustment (−2 to 0)

Apply a small penalty for older news within the 7-day window:

| Age | Adjustment |
|-----|-----------|
| 0–2 days | 0 |
| 3–4 days | −1 |
| 5–7 days | −2 |

### Total Score Formula

```
Total = Core Score (0–25) + Portfolio Relevance (0–5) + Time Decay (−2 to 0)
Range: −2 to 30
```

---

## Step 3 — Assign Rating & Signal Strength

### Rating

| Score | Rating | Label |
|-------|--------|-------|
| 22–30 | **A** | High Conviction |
| 18–21 | **B** | Relevant |
| 14–17 | **C** | Low Impact |
| < 14  | **D** | Noise |

### Signal Strength

Evaluate **in order** and stop at the first match. Every item gets a signal.

| # | Condition | Signal |
|---|-----------|--------|
| 1 | Score ≥ 22 **and** Portfolio Relevance ≥ 4 | 🔴 STRONG |
| 2 | Score ≥ 18 **or** Portfolio Relevance ≥ 3 | 🟡 MODERATE |
| 3 | anything else | ⚪ WEAK |

The earlier version of this table used three independent conditions and left holes: a
global macro shock with no portfolio exposure (Score 24, Relevance 2) matched none of
them, so an item rated **A / High Conviction** had no signal to print and the summary
counters did not sum to the item count. Ordered evaluation with a catch-all fixes that.

**Degraded mode — no universe file.** When Step 0 found no universe, Portfolio Relevance
is `n/a`, which makes rows 1 and 3 unreachable and would push everything into MODERATE.
Score on the core alone instead, and label the output:

| Core score (0–25) | Signal |
|---|---|
| ≥ 22 | 🔴 STRONG (macro only) |
| ≥ 18 | 🟡 MODERATE (macro only) |
| < 18 | ⚪ WEAK (macro only) |

**Carry the "(macro only)" label into every line of the output.** A STRONG that was never
checked against the portfolio must not read like one that was.

### Actionability Flag

For each item rated A or B, add one of:
- 🔍 **MONITOR** — Watch for follow-through
- ⚠️ **REVIEW** — Consider reviewing position/exposure
- ✅ **CONFIRMS** — Validates existing thesis
- ❌ **CONTRADICTS** — Challenges existing thesis

---

## Step 4 — Output Format

Present only **Top 3–7 items** (rating A or B). Drop D items entirely.
Include C items only if fewer than 3 items score A/B.

**Exception, and it overrides the drop rule:** if *every* item scores D, report the week
as low signal and list the top 3 anyway, marked as such. Returning nothing hides the
difference between "no news" and "no signal in this news", and those are not the same
finding.

Use this format for each item:

```
## [Rank]. [Headline]
**Date:** [date] | **Score:** [X/30] | **Rating:** [A/B/C] | **Signal:** [STRONG/MODERATE/WEAK]
**Actionability:** [flag + label]
**Assets Affected:** [list from investment universe, or "Broad universe"]

**Insight:** [1 paragraph — what happened, why it matters, what to watch next]

Score breakdown: Macro [X] | Surprise [X] | Market Rel. [X] | Forward [X] | Structural [X] | Portfolio [X] | Time [X]
```

### Summary Footer

After the ranked list, add:

```
---
### Weekly Signal Summary
- 🔴 Strong signals: [N]
- 🟡 Moderate signals: [N]
- ⚪ Weak/Noise: [N]
- Top theme this week: [1 sentence]
- Key risk to monitor: [1 sentence]
```

---

## Edge Cases

- **No news provided**: Ask the user to paste headlines or specify a time range
- **All items score D**: Report this — "Low signal week" — and list top 3 anyway
- **Breaking news (< 24h)**: Skip time decay, flag as [DEVELOPING]
- **Conflicting signals on same asset**: List both and note the contradiction
