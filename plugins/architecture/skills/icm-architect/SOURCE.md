# Source and provenance

This skill vendors the **icm-architect** Claude skill, sourced from
https://github.com/RinDig/icm-architect (MIT license, copyright Jake Van Clief),
which implements the **Interpretable Context Methodology** (ICM) —
Van Clief & McDermott, arXiv:2603.16021 — "folder structure as agent
architecture."

Fetched and vendored into this repo on 2026-08-19. `references/` and
`assets/templates/` are byte-identical to upstream. `SKILL.md` is the
upstream body with **two deliberate removals**:

1. The "Auto-use in this account" section, which made the skill apply by
   default to every new project without being asked.
2. The clause at the end of the description that did the same thing.

An earlier vendoring pass had *added* that section. It was removed because
it contradicted the skill's own guardrail — "a workspace for a thing done
twice is scaffolding, not architecture" — and the guardrail is now a
routing exclusion in the description instead. Eval case
`07-architecture-audit` exists to check that ICM is not over-applied.

Related upstream projects considered and not chosen for this vendoring
pass: `Naxxy/workspace-builder-skill` (a heavier 5-mode ICM implementation
with shell tooling — more moving parts than needed here) and
`ktnCodes/icm-template` (a plain folder template, not a packaged skill).

To refresh this vendored copy, re-fetch the files listed above from the
upstream repo, then **re-apply the two removals above**. Do NOT reinstate
the "Auto-use" section: it is the defect this vendoring pass corrected,
and re-adding it silently invalidates eval case `07-architecture-audit`.
