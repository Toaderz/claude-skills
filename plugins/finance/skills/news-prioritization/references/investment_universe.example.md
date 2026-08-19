# Investment universe — format example

**This is a format example, not data.** The real universe is personal holdings and does
not ship inside a plugin that other people install. It lives in the project that uses
this skill, at `.claude/investment_universe.md`.

The structure below is the contract the skill matches against.

---

## US

- Example Large Cap Fund
- Example Rising Dividend ETF
- S&P 500 PR

---

## Tech

- Example AI Thematic ETF
- Example Cybersecurity ETF
- NASDAQ Composite PR USD

---

## Emerging Markets

- Example EM Ex-China ETF
- MSCI EM PR USD

---

## Rules the format has to satisfy

- Every `##` heading is a **sector**. Its name is used for thematic matching.
- Every bullet under a heading is an **exact asset name**, matched literally.
- An asset may appear under more than one heading; the most specific sector wins.
- Broad index names (S&P 500, MSCI ACWI, NASDAQ) mark broad universe exposure.

Nothing else in the file is read. Comments, notes, and extra prose are ignored.
