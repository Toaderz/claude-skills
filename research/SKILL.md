---
name: news-prioritization
description: >
  Evaluates and ranks financial/macro news based on macro relevance, surprise
  factor, and direct impact on the tracked investment universe. Use this skill
  whenever the user asks to review, filter, rank, prioritize, or summarize
  recent financial news, macro developments, or market events — especially
  when they mention "weekly news", "what matters this week", "macro recap",
  "news for my portfolio", or similar. Also trigger when the user pastes a
  list of headlines or news items and wants to know which ones are important.
  Always use this skill before presenting any financial news summary.
---

# News Prioritization Skill

## Objective

Identify, evaluate, and rank the most relevant macro-financial news from the
last 7 days for the tracked investment universe. Output a clean, ranked list
with scores, ratings, signal strength, and one actionable insight per item.

---

## Step 0 — Load Investment Universe

Before scoring any news, read `investment_universe.md` to load:
- **Exact asset names** from `## Assets (Exact Match)` — use for direct matching
- **Sector mapping** from the sector sections — use for thematic matching

If the file is not available, ask the user to provide it or proceed with
general market knowledge and note the limitation.

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

Match the news against `investment_universe.md`:

| Score | Criteria |
|-------|----------|
| **5** | Direct impact on a specific named asset (exact match) |
| **4** | Strong sector impact affecting multiple assets in universe |
| **3** | Macro/thematic impact affecting broad universe exposure |
| **2** | Weak indirect relevance |
| **1** | Very distant relation |
| **0** | No relevance to the investment universe |

**Matching rules:**
- Match company names directly from `## Assets (Exact Match)`
- Match ETFs by their stated exposure (e.g., CIBR → cybersecurity news)
- Match sectors using the sector sections in the file
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

| Condition | Signal |
|-----------|--------|
| Score ≥ 22 AND Portfolio Relevance ≥ 4 | 🔴 STRONG |
| Score 18–21 OR Portfolio Relevance 3–4 | 🟡 MODERATE |
| Score < 18 AND Portfolio Relevance ≤ 2 | ⚪ WEAK |

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
