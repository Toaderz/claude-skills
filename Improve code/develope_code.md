---
name: python-dev-discipline
description: >
  Enforces disciplined Python development practices for projects with complex logic.
  Use this skill whenever the user is building, debugging, refactoring, or extending a
  Python project that involves multi-module architecture, data processing pipelines,
  iterative development, or any codebase where robustness matters more than speed.
  Trigger on phrases like "fix this bug", "add this feature", "refactor", "new module",
  "it's breaking", "doesn't work for this case", "write a parser/pipeline/detector",
  or any request to write Python code that touches more than one function.
  Also trigger when the user starts a new Python project from scratch, asks to implement
  an algorithm or technique, or asks "how should I do X?" for non-trivial problems.
  Do NOT trigger for one-off scripts, simple utilities, or questions about Python syntax.
---

# Python Development Discipline

Prevents the costliest mistakes in iterative Python development: regressions, hardcoding,
architecture drift, and untested code. Organized in three priority levels.

---

## Level 1 · Core Rules (always enforce)

These are non-negotiable. Apply on every code change, no exceptions.

### 1. No hardcoded fixes

Every fix must be a **general heuristic**, not a patch for one case.

Before proposing any fix, answer: **"Does this work for other inputs, or only this one?"**

Red flags: specific sheet/column/row names, `if value == "specific_string"`, magic numbers,
offsets assuming a layout. Instead: detect patterns ("≥30% numeric" not "column 5"), use
content-type signals, make thresholds configurable or data-derived.

> "That fix works here but breaks if [scenario]. Here's a general approach: [X]."

### 2. Respect module responsibility

Each module/class/function has one job. Detection doesn't go in builders. Formatting
doesn't go in parsers. Business rules don't go in core libraries.

> "This belongs in [module X] because [reason]. Should I put it there?"

### 3. Root cause first — never patch downstream

In any pipeline (`scan → detect → parse → normalize → build`), bugs often originate
upstream but manifest downstream. **Always trace the pipeline first** before writing
any fix.

Ask: "Is the problem in this component, or is it receiving bad input from earlier?"

Never fix symptoms in step 4 if the cause is in step 2. Walk the data backward until
you find where it first goes wrong, then fix there.

> "The output looks wrong here, but the actual issue is in [upstream module] which
> is passing [bad data]. Fixing it there instead."

### 4. Don't break interfaces

If a function returns `(data_cols, data_rows)`, keep that contract. Interface changes
cascade and cause subtle regressions. If a change is truly needed, flag it:

> "This requires changing [function]'s return type, affecting [callers]. Proceed?"

### 5. Regression tests before closing

Before any task is considered done:
- Run existing tests if they exist — new code must not break them
- Propose new tests for non-trivial changes: happy path + edge case + a test that
  would have caught the original bug
- If the user says "it works" but there are no tests:

> "Works for this case. Want me to add a test to lock this in before we move on?"

### 6. Complexity check

When a function exceeds **~50 lines**, flag it for review. But line count is just the
trigger — the real signals are:

- **Can't describe it in one sentence** → it has multiple responsibilities, split it
- **3+ levels of nested if/for** → extract inner logic into named functions
- **Multiple unrelated operations** → break into a pipeline of small, clear steps

Design functions to be **conceptual and easy to use**: the caller should understand
what a function does from its name and signature alone, without reading the body.
All complexity stays internal. Public APIs should be minimal and intuitive.

```python
# Good: caller understands intent immediately
tablas = detectar_tablas(hoja)
df = construir_dataframe(tabla, opciones)

# Bad: caller needs to know internals
result = process(sheet, 3, True, None, "horizontal")
```

---

## Level 2 · Workflow (follow on every task)

These are the steps to follow for each coding task, in order.

### Step 1 · Objective

Get a one-sentence goal. If the user hasn't stated one, ask:

> "In one sentence, what should this change accomplish?"

This is the **anchor**. Every decision gets measured against it.

### Step 2 · Component

Identify which module owns the responsibility. Read the relevant code first.
If the change would touch **3+ modules**, pause:

> "This affects [X], [Y], and [Z]. Likely a deeper issue. Diagnose root cause first?"

### Step 3 · Research

Before proposing a solution for anything non-trivial, **research current best practices**.

- Use web search to find modern approaches, maintained libraries, benchmarks
- Compare 2-3 options when the decision affects architecture or performance
- Present findings concisely with trade-offs
- If the user's approach is suboptimal, say so directly with the better alternative
- If research confirms the user's approach is solid, say so too

Skip research for simple, obvious tasks (sorting, file I/O, basic string operations).

### Step 4 · Code

Write the code following Level 1 rules. While coding, proactively flag:

- Code smells (duplication, unclear names, deep nesting)
- Future risks (brittle assumptions, tight coupling, missing error handling)
- Better libraries or techniques discovered during research
- Architectural improvements (extract utility, add config point, simplify pipeline)

> "This works, but I noticed [X]. Improve now or save for later?"

**Style:** descriptive names, comments explain *why* not *what*, documented thresholds,
vectorized operations over loops, no magic constants.

### Step 5 · Test

Run the generality check ("works for other cases?"), run existing tests, propose new
ones. Summarize: what changed, which files, any limitations, and confirm the objective
from Step 1 was met.

---

## Level 3 · Advanced Heuristics

For detecting subtle development anti-patterns that waste time. These are documented
in detail in `references/advanced_heuristics.md` — read that file when any of these
patterns are detected:

- **Scope creep** — user keeps adding "one more thing" beyond the objective
- **Yak shaving** — working on a dependency of a dependency of the real task
- **Overthinking** — 2-3 failed iterations on the same approach without convergence
- **Perfectionism** — excessive polishing of non-critical code
- **Repeated failures** — same error type recurring across attempts

The key intervention for overthinking (the most common one):

> "We've iterated [N] times on this approach and it keeps getting more complex.
> That usually means the approach itself isn't right. Let me try a different angle."

Pivot rules: (1) don't break existing working code, (2) stay aligned with the core
objective, (3) explain what the new approach changes fundamentally.
