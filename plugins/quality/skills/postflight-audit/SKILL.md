---
name: postflight-audit
description: >
  Verifies finished work before it is called done, at a depth proportional to what the
  change can break: a cold re-read for small edits, tests and an architecture check for
  ordinary changes, adversarial review and a security pass for anything reaching
  production. Use after substantive work is complete, before declaring a task finished,
  before opening a pull request, before a deploy or release, and on "ya quedó?",
  "revisa antes de cerrar", "is this ready", "ship it", "done?", "listo para producción".
  Do NOT use for trivial edits, for work still in progress, or as a substitute for
  reading the diff — the built-in /code-review already reviews code line by line.
---

# Postflight audit

The last thing between "it works" and "it is done".

**The job is to find reasons NOT to approve.** An audit that reports "looks good" without
naming what it checked has not audited anything — it has agreed.

---

## 1. Set the depth

Depth follows blast radius, not effort spent. **Running the maximum audit on a one-line
change is a cost with no buyer**, and it teaches everyone to skip the audit.

| The change | Depth | What runs |
|---|---|---|
| A typo, a comment, a constant | **none** | Re-read the diff. Say it is done. |
| One file, contained, reversible | **light** | Cold re-read · linter · the tests that touch it |
| Several files, real logic, shared code | **standard** | light + full test suite + does it belong where it was put |
| Production, migrations, auth, money, data loss, public API | **full** | standard + `critical-reviewer` + `/security-review` |

When the depth is uncertain, ask one question: **what is the worst thing this change can
do if it is wrong?** The answer picks the row.

## 2. The cold re-read

At every depth above `none`. Read the result as if you had not written it, without the
narrative momentum of having just built it:

- Does the result actually match what was asked, or what became convenient?
- Is the structure coherent to someone who was not here?
- Are the numbers, names, and paths internally consistent?
- Does every claim trace to something real — a run, a file, a source?
- Is anything required simply missing?
- Did an unsupported conclusion slip in?
- Does it still make sense read cold, with no prior context?

**This is the highest-yield step and the cheapest.** Most defects are visible on a second
honest read; they survive because nobody takes one.

## 3. Run the checks

Run the project's own tooling, whatever it is — the checks a contributor runs locally.
Find them before inventing any: `Makefile`, `package.json` scripts, `pyproject.toml`,
CI config.

- **Never report a check you did not run.** "Tests should pass" is not a result.
- **Paste the failure, not a summary of it**, when something fails.
- If a check cannot run here (missing dependency, no credentials, no network), say which
  one and why. A skipped check reported as skipped is fine; a skipped check reported as
  passing is a lie.

## 4. Delegate the adversarial pass — `full` only

At `full` depth, delegate to the `critical-reviewer` subagent. Its isolation is the
mechanism: it never saw your reasoning, so it cannot inherit your blind spot, and it is
read-only, so it cannot quietly fix a thing and call it fine.

Then run the built-in `/security-review`. **Do not write a security agent** — it exists
and it is maintained upstream.

One reviewer is the default. A second only when the change spans genuinely independent
domains and one reviewer would have to context-switch to cover both.

## 5. Report

State the depth you chose and why. Then, in order:

1. **What was checked** — named, with results
2. **What failed** — with the actual output
3. **What was not checked** — and why
4. **What is still uncertain** — the parts you could not verify
5. **The verdict** — done, or done except X

Valid verdicts are **"done"**, **"done except X"**, and **"not done"**. If nothing was
found, say what was checked so the "nothing" carries weight:

> "Standard depth. Ran `pytest -m 'not slow'` (86 passed) and `ruff` (clean). Re-read the
> diff cold: the retry path swallows `TimeoutError`, which is deliberate here but is not
> written down anywhere. Not blocking. Untested: the slow suite needs a live DB. Done."

---

## Rules

1. Depth follows blast radius. Auditing everything at maximum is how audits stop happening.
2. Look for reasons not to approve. Agreement is not verification.
3. Never report a check you did not run.
4. Paste failures; do not summarise them away.
5. Name what you could not check. Silence reads as coverage.
6. One adversarial reviewer, and only when the risk earns it.
7. `/security-review` and `/code-review` are built in. Use them; do not rebuild them.
8. "It works" is a claim about one run. "It is done" is a claim about the next one.
