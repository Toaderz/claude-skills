---
description: Audit finished work before calling it done — depth proportional to what it can break
argument-hint: [what to audit, or blank for the current work]
---

Audit the following work before it is called done, following the `postflight-audit`
skill.

**Target:** $ARGUMENTS

If the target above is empty, audit the work most recently completed in this session.

Since this was invoked explicitly, show the audit:

1. **Depth and why** — none, light, standard, or full, justified by what the change
   can break if it is wrong. Not by how much effort went into it.
2. **Cold re-read** — what you found reading the result as a stranger: mismatches with
   the actual request, incoherent structure, inconsistent numbers or paths, claims that
   trace to nothing, missing pieces, conclusions that outran their evidence.
3. **Checks run** — each one named, with its real output. Find the project's own
   tooling first; do not invent commands it does not have.
4. **Failures** — pasted, not summarised.
5. **Not checked** — every check you skipped and the reason. A skipped check reported
   as skipped is fine. Reported as passing, it is a lie.
6. **Adversarial pass** — at `full` depth only: delegate to `critical-reviewer`, then
   run the built-in `/security-review`. State the findings, including the ones you
   disagree with and why.
7. **Still uncertain** — what you could not verify from here.
8. **Verdict** — `done`, `done except X`, or `not done`.

**Your job is to find reasons not to approve.** If you find nothing, say exactly what
you checked, so the "nothing" means something.

Do not fix what you find unless asked. The audit is the deliverable.
