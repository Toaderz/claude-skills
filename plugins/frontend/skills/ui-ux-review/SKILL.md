---
name: ui-ux-review
description: >
  Reviews an interface for the things that break real users: keyboard and screen-reader
  access, contrast, visual hierarchy, behaviour at small widths, component structure, and
  consistency with the design system already in the codebase. Use when asked to review,
  critique, or improve a UI, component, page, or screen, when accessibility is in
  question, when something "feels off" visually, and on "revisa esta interfaz", "está
  accesible", "se ve mal en móvil", "review this component", "a11y check", "responsive
  issues". Do NOT use to build a site from scratch, to design a chart or dashboard, or
  for backend and data-layer work with no rendered surface.
---

# UI/UX review

Review what a user hits, in the order they hit it. Most interface defects are not
aesthetic — they are a keyboard trap, a 3:1 contrast ratio, or a table that vanishes at
390px.

**Do not rebuild what already exists.** Charts and data displays belong to the built-in
`dataviz` skill; standalone visual artifacts belong to `artifact-design`. This skill
reviews interfaces in a codebase and points at those instead of duplicating them.

---

## 1. Access first

The failures here lock people out entirely, so they outrank everything below.

- **Keyboard**: every interactive element reachable by Tab, in an order that matches the
  visual one. A visible focus ring. No trap — including in modals and menus.
- **Semantics**: real `<button>`, `<a>`, `<label>`, `<nav>`, headings in order. A `<div>`
  with an `onClick` is invisible to assistive technology and to the keyboard.
- **Names**: every control and image has an accessible name. Icon-only buttons need one
  explicitly.
- **Contrast**: 4.5:1 for body text, 3:1 for large text and interactive boundaries.
  **Measure it — do not eyeball it.**
- **Not colour alone**: state must survive colour blindness and greyscale.
- **Motion**: honour `prefers-reduced-motion`.
- **Live regions**: content that changes without navigation must announce itself.

## 2. Hierarchy

- Is the primary action the most prominent thing on the screen? Exactly one per view.
- Does size, weight, and spacing encode importance, or decoration?
- Is related content grouped by proximity, before any border is added?
- Does the eye land where the task starts?

## 3. Behaviour under stress

Interfaces are designed at 1440px with three rows of clean data. They fail elsewhere:

- **Narrow** — 320–390px. Tables, wide charts, and long words are where it breaks.
- **Empty** — no data yet. Does it explain what goes here, or show a blank box?
- **Loading** — is there feedback before content arrives, and does the layout hold still?
- **Error** — does it say what happened and what to do, or print a stack trace?
- **Overflow** — a 90-character name, 400 rows, a missing image.
- **Slow and offline** — what does a 3-second request look like?

**An interface that only works on the happy path is a demo.**

## 4. Structure and consistency

- Are components split by responsibility, or by where they happened to be written?
- Is state held at the right level, or threaded through five props?
- **Does the codebase already have this component?** A second variant of a button is a
  defect, not a feature.
- Do spacing, colour, radius, and type come from tokens, or from magic numbers?
- Does it match the conventions already in this repository — even the ones you would not
  have chosen? Consistency beats local preference.

## 5. Report

Order findings by what they cost a user, not by how easy they are to fix:

1. **Blocking** — someone cannot complete the task: keyboard trap, unlabelled control,
   failing contrast on body text
2. **Damaging** — the task is possible but painful: broken at narrow widths, no error
   state, hierarchy fighting the task
3. **Worth fixing** — inconsistency, duplication, magic numbers
4. **Preference** — say so explicitly, and keep it short

For each: **what it is, who it hurts, and the smallest fix.** Cite `file:line`.

Say what is already good, briefly and specifically. A review that is only findings gets
read as noise the second time.

---

## Rules

1. Access before aesthetics. A keyboard trap outranks any spacing.
2. Measure contrast; never estimate it.
3. Empty, loading, error, and overflow are states, not edge cases.
4. Check 320px before anything else responsive.
5. Search for the existing component before proposing a new one.
6. Tokens over magic numbers; repo convention over personal taste.
7. Rank by user cost, not by fix cost.
8. Label preference as preference.
9. Charts go to `dataviz`, standalone visuals to `artifact-design`. Do not rebuild them.
