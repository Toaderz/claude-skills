---
name: project-structure-governor
description: "General-purpose project organization and workflow governance skill. Use for any repository when Claude needs to set up or maintain a clean project structure, separate context from data and examples, define or refine the working flow, detect whether research, examples, or extra context are actually needed, keep the repo organized after each iteration, and update `CLAUDE.md` to reflect the current project components, folders, skills, and workflow."
---

# Project Structure Governor

Assume `claude-optimization` is active.
Use this skill for any project, not just a domain-specific repository.

This skill governs:

- project organization
- folder separation
- flexible workflow selection
- `CLAUDE.md` maintenance
- end-of-iteration hygiene checks

## Mandatory bootstrap

Before starting work in any project that uses this skill, ensure the base local skills are present in `.claude/skills/`.

These base skills are mandatory and should be carried over as-is:

- `claude-optimization`
- `find-skills`
- `workflow-orchestrator`
- `project-structure-governor`

Treat this bootstrap as rigid.
Do this before substantive work begins.

If the target project does not contain these local skills yet:

1. create or populate `.claude/skills/`
2. copy or recreate the mandatory base skills
3. confirm that `CLAUDE.md` reflects the active base skills
4. only then continue with project-specific work

## Core responsibilities

1. Detect what kind of project this is.
2. Decide which structural components are needed.
3. Create or refine a clean folder layout.
4. Separate context, data, examples, assets, and executable logic.
5. Detect whether the task really needs research, examples, or additional skills.
6. Keep `CLAUDE.md` synchronized with the real state of the repository.
7. Check at the end of each iteration whether the work is still well organized.

## Flexible workflow detection

Do not force the same flow on every project.
First detect which of these layers are relevant:

- context
- data
- examples
- research
- skills
- assets
- scripts
- outputs

Use only the layers that the project actually needs.

Examples:

- a coding utility may need scripts, examples, and outputs, but no research
- a research repo may need context, data, examples, and sources
- a design repo may need assets, examples, and brand context
- a simple one-off automation may need almost no context structure

## Baseline operating sequence

1. Ensure the mandatory `.claude/skills/` bootstrap exists.
2. Activate `claude-optimization`.
3. Inspect the current repo state.
4. Classify the project type.
5. Decide the minimum useful structure.
6. Check whether there are local skills that already solve part of the work.
7. Detect whether context, data, examples, research, assets, or scripts are needed.
8. Create or refine the structure.
9. Update `CLAUDE.md` to reflect the current repo accurately.
10. After each iteration, run an organization check.
11. Before final delivery, verify that the repo structure and the output still match.

## Organization rules

Keep different kinds of information separate whenever the project is large enough to justify it.

Typical categories:

- `contexto/` or `context/`: reusable project knowledge
- `datos/` or `data/`: datasets, inputs, exports, structured sources
- `ejemplos/` or `examples/`: prompts, samples, outputs, reference deliverables
- `assets/`: non-text resources used in outputs
- `scripts/`: deterministic helpers or automations
- `.claude/skills/`: local skills

Do not force Spanish or English folder names.
Prefer the naming convention already used by the repository unless the repo is still being initialized.

## CLAUDE.md maintenance

Use `CLAUDE.md` as the live operating map of the repository.
Keep it current when project structure changes.

Only update the sections that describe repo state and workflow.
Do not rewrite unrelated user-authored guidance unless it is clearly stale and directly conflicts with reality.

Maintain these kinds of sections when appropriate:

- project objective
- base skills
- active structure
- active skills
- workflow
- current components
- organization rules

If `CLAUDE.md` does not exist, create it.
If it exists, update it incrementally.

For section guidance, read `references/claude-md-schema.md`.

## Component tracking

Whenever files, folders, skills, workflows, or major project components are added or removed:

1. Check whether `CLAUDE.md` should reflect the change.
2. Update the relevant inventory or structure section.
3. Remove references that are no longer true.
4. Keep the summary concise and operational.

Track components at the right level.
Do not list every tiny file.
Prefer meaningful units such as:

- research area
- data pipeline
- deck template
- parser module
- reporting workflow
- local skill

Always keep the mandatory base skills visible in `CLAUDE.md` when this skill governs the project.

## Iteration-end organization check

At the end of each meaningful iteration:

1. Check whether new files were placed in the right folders.
2. Check whether context, data, and examples were mixed incorrectly.
3. Check whether the mandatory base skills are still present.
4. Check whether new skills were documented.
5. Check whether empty or redundant structure was introduced.
6. Check whether `CLAUDE.md` still matches the repo.
7. Fix small organization problems immediately.

If a structural issue is too ambiguous to fix safely, surface it explicitly.

## Missing-piece detection

Use explicit labels:

- `Falta contexto`
- `Faltan datos`
- `Faltan ejemplos`
- `Falta skill`
- `Falta estructura`

Do not ask for missing pieces unless they are actually required.
Absence of examples is not automatically a blocker.
Absence of research is not automatically a blocker.

## Skill routing

If the project needs domain or task-specific skills:

1. Check local skills first.
2. If none fit, use `find-skills` before improvising a repeated workflow.
3. Only recommend or install verified external skills.

## Final verification

Before completing the task, verify both:

1. the deliverable
2. the repo organization produced around it

Check:

- structure still makes sense
- `CLAUDE.md` matches reality
- mandatory base skills are present
- files live in the right place
- no obvious category mixing remains
- workflow documentation still fits the project

If the project changed during the task, the repository map must change with it.
