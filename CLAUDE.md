# AI Engineering OS

This repository **is** a Claude Code plugin marketplace. It ships engineering-discipline
capabilities that install into other projects.

Working *on* this repo? Read [`docs/architecture.md`](docs/architecture.md) first.

## Layout

| Path | What |
|---|---|
| `.claude-plugin/marketplace.json` | the marketplace manifest — 7 plugins |
| `plugins/<name>/` | one plugin: `skills/`, `agents/`, `commands/`, `evals/` |
| `registry/` | human inventory of every capability. **Not a router** |
| `docs/` | architecture, capability policy, audit, measurements |
| `scripts/` | `validate.sh`, `measure.sh`, `init-project.sh` |

## What lives where

`core-discipline` planning and project memory · `quality` completion gate ·
`engineering` Python and module architecture · `architecture` ICM workspaces ·
`frontend` UI review and web design · `research` research and decisions ·
`finance` market news triage.

**Routing is not configured here.** Claude Code matches on each skill's own
`description`; this file does not tell anyone which skill to read. If a skill fires when
it should not — or fails to fire — fix its description, not this file. See
`docs/routing-tests.md` §4 for the diagnosis order.

## Rules for changing this repo

1. **Do not duplicate what Claude Code already does.** Pass the gate in
   [`docs/adding-capabilities.md`](docs/adding-capabilities.md) before adding anything,
   and state in the PR which built-in you considered and why it does not cover the case.
2. **`scripts/validate.sh` must be green** before every commit: 0 errors, 0 warnings.
3. **Measure before adding to `core-discipline`.** Its cost is paid in every session
   forever. `scripts/measure.sh` gives the real number.
4. **Zero additional monetary cost.** No `claude plugin eval`, no paid graders, no paid
   APIs. A test that would cost money is written and reported as
   `not executed — cost prohibited`.
5. **This repository is public.** No personal data, credentials, or holdings in the tree.

## Working in a project that installed these

Nothing to configure. The plugins are installed, their descriptions are loaded, and
Claude Code routes to them. `scripts/init-project.sh` installs the right ones for a
project; `--dry-run` shows what it would do first.
