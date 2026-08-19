# Source and provenance

This skill vendors the **icm-architect** Claude skill, sourced from
https://github.com/RinDig/icm-architect (MIT license, copyright Jake Van Clief),
which implements the **Interpretable Context Methodology** (ICM) —
Van Clief & McDermott, arXiv:2603.16021 — "folder structure as agent
architecture."

Fetched and vendored into this repo on 2026-08-19. Content is copied
near-verbatim from the upstream `SKILL.md`, `references/`, and
`assets/templates/`, with one addition: the "Auto-use in this account"
section at the end of `SKILL.md`, which wires this skill into this
repo's root `CLAUDE.md` so it runs by default on every new project
instead of requiring an explicit request each time.

Related upstream projects considered and not chosen for this vendoring
pass: `Naxxy/workspace-builder-skill` (a heavier 5-mode ICM implementation
with shell tooling — more moving parts than needed here) and
`ktnCodes/icm-template` (a plain folder template, not a packaged skill).

To refresh this vendored copy, re-fetch the files listed above from the
upstream repo and re-apply the "Auto-use" addition.
