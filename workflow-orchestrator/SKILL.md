---
name: workflow-orchestrator
description: "Orchestrate task execution in this repository after claude-optimization is active. Use for research, analysis, organization, presentation creation, data-driven deliverables, or any task that must choose the right local skill, inspect context, check data, review examples, identify missing inputs, search for verified external skills when needed, and validate the final result before delivery."
---

# Workflow Orchestrator

Assume `claude-optimization` is already active.
Use this skill as the default execution flow for non-trivial tasks in this repository.

## Core sequence

1. Understand the task and classify it.
2. Detect whether a local thematic skill applies.
3. Read only the minimum relevant local context.
4. Check whether the needed data already exists.
5. Check whether useful examples already exist.
6. Identify what is missing:
   - context
   - data
   - skill
   - example
7. Resolve missing pieces in the right order.
8. Execute the task.
9. Run a final cold verification before delivery.
10. Deliver the result.

## Execution order

### 1. Classify the task

Classify the request as one or more of:

- research
- organization
- analysis
- comparison
- presentation
- skill creation
- data preparation

This classification determines which context and skills to inspect.

### 2. Detect the right skill

Check local skills first in:

- `.claude/skills/`
- `.agents/skills/`

If a local skill is sufficient, use it.
Do not search externally unless the local repo lacks a suitable skill.

If no local skill fits:

1. Use the local `find-skills` skill as the mandatory discovery path before improvising or proceeding without a skill.
2. Search for an external skill only if the task is repeated enough to justify it.
3. Prefer trusted and verified sources.
4. Reject weak, unclear, or low-trust skills.
5. If a verified skill is found and it materially improves repeated work, recommend it and install it only when appropriate.
6. If no reliable skill exists, proceed with the best direct workflow and say that no verified skill was available.

### 2A. External skill policy

When the repository lacks a sufficient local skill:

1. Activate `find-skills`.
2. Search for a skill that matches the task.
3. Verify quality before recommending or installing:
   - trusted source
   - meaningful install count when available
   - credible repository quality
   - clear fit for the task
4. Prefer recommendation over automatic installation by default.
5. Install automatically only when all of these are true:
   - the skill is verified
   - the task is likely to recur
   - the skill clearly improves execution quality or speed
   - installation is feasible in the environment
6. If installation is not justified, continue with the best direct workflow and note that no install was performed.

### 3. Read minimum context

Inspect only the relevant files in `contexto/`.
Do not bulk-read the entire folder.

Typical mapping:

- presentation narrative -> `contexto/investigacion/presentacion-etfs.md`
- professional comparisons -> `contexto/investigacion/comparativas-etfs-pro.md`
- Claude slide workflow -> `contexto/investigacion/skills-claude-presentaciones.md`

If context is still insufficient, state exactly what is missing before asking the user for more.

### 4. Check data

Inspect `datos/` for existing inputs before asking for anything.

Examples of missing data:

- benchmark returns
- holdings
- expense ratio
- AUM
- drawdown
- factsheets
- comparable products

If data is missing and the task depends on it:

1. Say exactly what is missing.
2. Explain why it matters.
3. Use external research only when appropriate.
4. Prioritize primary and trusted sources.

### 5. Check examples

Inspect `ejemplos/` for format references, prompts, outlines, or prior deliverables.

If no example exists:

- do not block
- create the strongest first version using current context and research

### 6. Execute

Work with the selected skill, available context, available data, and available examples.

Keep distinctions explicit:

- missing context is not missing data
- missing data is not missing skill
- missing example is not a blocker

### 7. Final cold verification

Before delivery, verify the result in a second pass without leaning on narrative momentum or the earlier reasoning path.

Check:

- result matches the task
- structure is coherent
- data is internally consistent
- claims align with the cited or available sources
- no required section is missing
- no unsupported conclusion slipped in
- output still works if read fresh with minimal prior context

This final review is meant to reduce overthinking bias and confirmation bias.

If the verification fails, fix the output before delivery.

## Escalation rules

Use explicit labels when blocked:

- `Falta contexto`
- `Faltan datos`
- `Falta skill`
- `Falta ejemplo`

Never say only "falta informacion".
Name the exact missing piece and its impact.

If the missing piece is `Falta skill`, explicitly state whether:

- a local skill exists but is insufficient
- `find-skills` found verified external options
- no verified external skill was found

## Source quality

For external research, prioritize:

- official fund documents
- prospectuses
- factsheets
- issuer sites
- regulatory sources
- reputable market data providers

Avoid basing decisions on low-trust summaries when primary material is available.
