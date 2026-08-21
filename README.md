# AI Engineering OS

A Claude Code plugin marketplace of engineering-discipline capabilities: plan before
executing, remember what matters, review adversarially, and finish deliberately.

**This repository is the source of truth.** Install from it; do not copy skills out of it.

---

## Install

```bash
git clone https://github.com/Toaderz/claude-skills.git
cd claude-skills

# Once, everywhere: planning, project memory, adversarial review, /preflight
claude plugin marketplace add ./ --scope user
claude plugin install core-discipline@ai-engineering-os --scope user

# Per project: install what that project actually needs
bash scripts/init-project.sh --dry-run /path/to/project   # see what it would do
bash scripts/init-project.sh /path/to/project
```

`init-project.sh` detects Python and frontend projects and installs `core-discipline` and
`quality` everywhere. It is idempotent, it fails with a clear message, and it never
silently overwrites an existing `.claude/settings.json`.

`research`, `architecture`, and `finance` are **not** auto-detected — nothing on disk says
a project does research or follows markets — so ask for them:

```bash
bash scripts/init-project.sh --only research,architecture /path/to/project
```

### Claude Code on the web: `--with-hook`

The instructions above assume `~/.claude` persists between sessions — true on a local
install, false on the web. There, every session is a **fresh, ephemeral container**:
nothing installed today survives to the next one except what gets committed to the
project's own repo.

Add `--with-hook` once, per project, and commit the result:

```bash
bash scripts/init-project.sh --with-hook /path/to/project
git -C /path/to/project add .claude/hooks .claude/settings.json
git -C /path/to/project commit -m "Install AI Engineering OS plugins on session start"
```

This writes `.claude/hooks/session-start.sh` — a `SessionStart` hook that re-registers
the marketplace and reinstalls this project's detected plugins at the start of *every*
future session, in *any* container, with nothing asked of you or of Claude. The
marketplace is referenced by its GitHub source (`Toaderz/claude-skills`), not a local
path, precisely so it resolves in a container that never saw this one.

One command, once, at project creation — after that, genuinely zero-ask.

---

## The honest trade-off

**"Zero commands per project, forever" is not achievable**, and any claim otherwise is
worth distrusting. Plugins install at a scope: `user` loads everywhere, `project` loads in
one place. A plugin is also the unit of installation, so **skills inside a plugin cannot
be scoped separately**.

That leaves a hybrid: the universal core at user scope, domains per project. One command
per project, not zero.

The reason is the measured cost. Every installed plugin's descriptions are resident in
every session at that scope:

| Plugin | Always-on | Contents |
|---|---:|---|
| `core-discipline` | ~640 tok | preflight-planning, project-memory, critical-reviewer, /preflight |
| `frontend` | ~481 tok | diseno-web-estrategico, ui-ux-review |
| `engineering` | ~478 tok | python-dev-discipline, deep-module-architecture |
| `research` | ~426 tok | deep-research, decision-comparison |
| `architecture` | ~293 tok | icm-architect |
| `quality` | ~246 tok | postflight-audit, /postflight |
| `finance` | ~233 tok | news-prioritization |

**Everything at user scope is ~2,797 ambient tokens in every session, forever.** A
repository with no Python, no UI, and no market exposure should pay 640, not 2,797. That
gap is what the per-project step buys.

Measure it yourself — the numbers come from the CLI, not an estimate:

```bash
bash scripts/measure.sh
```

---

## What is here

| Plugin | Scope | Capabilities |
|---|---|---|
| `core-discipline` | user | Plan before executing, with an agent budget that starts at zero. Durable project memory in `.claude/memory/`. A read-only adversarial reviewer. |
| `quality` | project | A completion gate whose depth follows what the change can break, and which looks for reasons *not* to approve. |
| `engineering` | project | Python discipline: general fixes over hardcoded patches, root-cause tracing. Deep-module architecture review. |
| `architecture` | project | ICM — folder structure as agent architecture (Van Clief & McDermott, MIT). |
| `frontend` | project | Accessibility-first interface review. Strategic web design. |
| `research` | project | Research with source tiers and a stopping criterion. Option comparison that states criteria before the verdict. |
| `finance` | project | Macro news triage against a tracked investment universe. |

11 skills, 1 agent, 2 commands. **One agent, not a fleet** — the other two candidates were
rejected: a security agent would duplicate the built-in `/security-review`, and a test
agent's context isolation is a cost, not a benefit, because it never saw what you just
built.

---

## What this does *not* do

**It does not build a router.** Claude Code matches on each skill's `description`; that
mechanism is the router. If a skill misfires, the fix is its description, its scope, or
its frontmatter — in that order. `docs/routing-tests.md` §4 has the full diagnosis
sequence. A routing miss is not a reason to build a router.

**It does not duplicate built-ins.** No document skills (`docx`/`pdf`/`pptx`/`xlsx`
exist), no code reviewer (`/code-review`), no security auditor (`/security-review`), no
chart skill (`dataviz`), no email skill (the official connector). See
[`docs/capability-policy.md`](docs/capability-policy.md).

**It installs no MCP servers.** Browser, email, and media options are documented in
[`integrations/`](integrations/) with their real per-request cost, so installing one is a
decision rather than an accident.

---

## Verification, and its limits

Everything free and local has been run:

```bash
bash scripts/validate.sh   # manifests, links, duplicates, registry, trigger matrix
```

Currently green: 0 errors, 0 warnings, all 12 routing scenarios covered, every expected
skill winning its own scenario.

**Semantic routing precision and recall are NOT verified.** Measuring them requires
`claude plugin eval`, which runs real agents and LLM graders and therefore costs money;
this project's policy forbids operations that create additional billing. The twelve eval
cases are written and committed but never executed, with the exact command in
[`docs/routing-tests.md`](docs/routing-tests.md).

The static trigger matrix in that document counts words. **It is a proxy, not proof**, and
is not offered as evidence that routing works.

---

## Documentation

| Document | For |
|---|---|
| [`docs/architecture.md`](docs/architecture.md) | the structural contract and the cost policy |
| [`docs/capability-policy.md`](docs/capability-policy.md) | the DO NOT DUPLICATE gate |
| [`docs/adding-capabilities.md`](docs/adding-capabilities.md) | how to add something, and what to justify |
| [`docs/routing-tests.md`](docs/routing-tests.md) | every measurement, and everything unmeasured |
| [`docs/audit-2026-08.md`](docs/audit-2026-08.md) | the pre-restructure baseline, frozen |
| [`docs/environment-notes.md`](docs/environment-notes.md) | what the runtime does and does not provide |
| [`registry/REGISTRY.md`](registry/REGISTRY.md) | inventory of every capability. **Not a router** |

## Licence

`icm-architect` derives from Interpretable Context Methodology (Van Clief & McDermott,
arXiv:2603.16021), MIT licensed; attribution is preserved in the skill's `SOURCE.md` and
`LICENSE`.
