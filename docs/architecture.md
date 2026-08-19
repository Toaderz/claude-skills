# Architecture

How this repository is organized, why it is organized that way, and which constraints are not
negotiable. Read this before adding, moving, or removing anything.

The audit that motivated this design is in [`audit-2026-08.md`](audit-2026-08.md).
The gate every new capability must pass is in [`capability-policy.md`](capability-policy.md).

---

## The goal

Not "make Claude use all the skills automatically." The goal is:

> **Discover the right capability, load the minimum necessary context, and run tools or agents
> only when the problem justifies it.**

Those three clauses pull against each other. More skills installed means better recall and worse
precision and more ambient cost. The architecture is the set of choices that trades between them
deliberately instead of accidentally.

---

## The repository is a plugin marketplace

```
GitHub repo  →  marketplace  →  plugins  →  projects
```

`.claude-plugin/marketplace.json` at the root makes this repo installable directly:

```bash
claude plugin marketplace add Toaderz/claude-skills
claude plugin install core-discipline@ai-engineering-os --scope user
```

**The repository is the single source of truth.** The same capability must not also live as a
hand-maintained copy in `~/.claude/skills/` or as a separately-edited skill on claude.ai. The
audit found five files byte-identical across repo and account — each one is a future divergence
and a double-load. Retiring those account copies requires the claude.ai UI and is listed in the
audit as work only the account owner can do.

### Layout

```
claude-skills/
├── .claude-plugin/marketplace.json     # makes the repo installable
├── CLAUDE.md                           # routing only, no capability logic
├── README.md
├── plugins/
│   ├── core-discipline/                # USER scope — the only always-on plugin
│   │   ├── .claude-plugin/plugin.json
│   │   ├── skills/
│   │   ├── agents/
│   │   ├── commands/
│   │   └── evals/                      # case definitions; see "Verification"
│   ├── quality/                        # PROJECT scope, candidate for USER
│   ├── engineering/                    # PROJECT scope
│   ├── architecture/                   # PROJECT scope
│   ├── frontend/                       # PROJECT scope
│   ├── research/                       # PROJECT scope — domain-neutral
│   └── finance/                        # PROJECT scope — domain-specific by design
├── integrations/                       # how to reach tools we deliberately did not wrap
├── registry/                           # human inventory — never loaded at runtime
├── docs/
└── scripts/
```

Component directories (`skills/`, `agents/`, `commands/`) live at the **plugin root**, not inside
`.claude-plugin/`. Only the manifest goes in `.claude-plugin/`.

---

## No custom router

Claude Code already routes. At startup it preloads each skill's `name` and `description` — nothing
else — and loads the body only when a request matches. That mechanism is free and already
maintained.

**A custom runtime router would add ambient token cost to duplicate it.** So it is not built.

When routing goes wrong, work this order:

1. **Description quality.** Almost always the answer.
2. **Installation and scope.** Is the plugin installed where the work happens?
3. **Frontmatter correctness.** Malformed frontmatter makes a skill invisible.
4. **`paths:` globs**, where they genuinely help.
5. **Project/domain scoping.** Move the capability closer to the work.
6. **Only if native routing proves insufficient** — investigate further.

Never built:

- a second runtime router
- a registry that gets read into context on every task
- a mandatory routing script
- redundant runtime orchestration on top of the `Agent` tool

`paths:` is reinforcement, never the sole discovery mechanism —
[issue #49835](https://github.com/anthropics/claude-code/issues/49835) can make a `paths`-scoped
skill undiscoverable entirely.

---

## Scope: USER vs PROJECT

> **USER** = useful in essentially any project.
> **PROJECT** = depends on the kind of work.

**A plugin is the unit of installation.** Individual skills inside a plugin cannot be scoped
separately. That constraint drives the whole layout: a capability's plugin *is* its scope
decision.

The initial USER-scope core is deliberately small:

```
core-discipline/
└── skills/
    ├── preflight-planning/
    └── project-memory/
```

Everything else starts at PROJECT scope and earns promotion by measurement.

| Capability | Plugin | Initial scope | Promotion rule |
|---|---|---|---|
| `preflight-planning` | core-discipline | USER | universal by definition |
| `project-memory` | core-discipline | USER | universal by definition |
| `postflight-audit` | quality | PROJECT | promoted only if the measured core stays within target |
| `icm-architect` | architecture | PROJECT | not universal; promoted only if trimmed and the core stays within target |
| engineering / frontend / research skills | respective | PROJECT | domain-specific by nature |
| `news-prioritization` | finance | PROJECT | **never promoted.** It scores news against a tracked investment universe; in a project that does not follow markets it is pure ambient cost with a routing rival attached. It is also the one capability coupled to user data, which is why the universe file is read from the project and not bundled |

### The context target

**Target: ≤600 ambient tokens for the USER-scope core.**

This is a *target*, not a runtime limit. **The measured value is reported as measured**, whatever
it turns out to be — `scripts/measure.sh` wraps `claude plugin details`, which reports a projected
token cost statically and for free.

The decision about what lives at USER scope weighs: actual metadata size · routing value ·
activation frequency · duplication · marginal token cost.

**If the core exceeds the target, useful capabilities are not deleted to hit a number.** The
procedure is:

1. measure;
2. identify the highest-cost, lowest-value capability;
3. move it to PROJECT scope **or** reduce its metadata;
4. re-measure.

The goal is minimum *useful* context, not minimum tokens at any cost. Routing quality is not
sacrificed to satisfy an arbitrary figure.

### Installation model, and its honest cost

| What | Scope | When |
|---|---|---|
| `core-discipline` | user | once; applies everywhere |
| everything else | project | `scripts/init-project.sh` |

**"Zero commands per project, forever" is not achievable** with the real plugin architecture.
`--scope user` would load every domain plugin into every project; `--scope project` requires a
command. The hybrid minimizes the cost rather than pretending it away: the global core is always
present, and domain capabilities cost one `init-project.sh` run per project.

`init-project.sh` must be idempotent, must fail with a clear message, and must never silently
overwrite user configuration.

---

## The registry is not a router

`registry/registry.json` records, per capability: name, type, plugin, path, purpose, triggers,
dependencies, required tools, scope, cost characteristics, what it replaces, and status.

It exists for **humans and maintenance** — discovery, auditing, dependency tracking, inventory.
**Claude never reads it per request.** A registry loaded into context on every task would be
exactly the custom router this architecture refuses to build.

---

## Agents

**Never spawn an agent simply because an agent exists.**

Every agent must have a clearly defined mission, a reason it adds value, a bounded scope,
appropriate tools, a measurable expected benefit, and a stopping condition.

**Prefer one agent when one suffices.** Use more only when the work genuinely decomposes,
isolation adds value, parallelism adds value, and the combined context and cost are justified.
Never a default fleet.

Do not optimize for maximum agent usage. Optimize for **maximum useful work per token and per
tool call.**

The repository ships **one** agent, `critical-reviewer`. Isolation is its mechanism, not an
incidental property: it cannot see the reasoning that produced the work, so it cannot be anchored
by it, and it is read-only so it cannot fix a problem and then declare the work sound.

`security-auditor` and `test-engineer` were considered and **deferred** — the first duplicates the
built-in `/security-review`, and for the second, context isolation is a cost rather than a benefit
(an agent that did not see what was just built writes worse tests than the main agent that did).
Adding either requires passing the gate in `capability-policy.md` with written justification.

---

## Cost policy

**This project must generate no additional monetary charges.**

Not allowed: paid API calls · external paid services · external LLM graders · evaluations that
create additional billing · services requiring payment credentials · operations whose monetary
cost is unknown · `claude plugin eval` where it incurs additional billing.

Allowed: deterministic local scripts · static validation · filesystem inspection · git operations ·
local token estimation · plugin validation · local routing heuristics · Claude Code functionality
already included in the user's existing plan.

**"Zero additional monetary charges" does not mean "zero use of the Claude Code allowance you
already have."** Using included functionality is fine as long as it creates no additional billing.

**If an operation's monetary cost is uncertain, it is not executed.** Prefer deterministic local
validation. The test is still written, and reported as `NOT EXECUTED — cost prohibited`.

A side benefit: `claude plugin eval` publishes its HTML report to claude.ai by default. Not
running it means nothing is published.

---

## Verification, and its limits

### What local, free, static checks establish

`scripts/validate.sh` (wrapping `claude plugin validate --strict` plus repo-specific lint) and
`scripts/measure.sh` (wrapping `claude plugin details`) verify:

valid skill structure · valid frontmatter · descriptions within limits · trigger coverage ·
`paths` · plugin manifests · scopes · duplicate detection · broken links · dependency references ·
registry consistency · installation · idempotency · approximate context footprint ·
deterministic routing heuristics

Targets: 0 invalid manifests · 0 broken links · 0 accidental duplicates · 0 orphan registry
entries · 0 unresolved dependencies.

### What they do not establish

Without a real runtime evaluation, this project **cannot claim measured** routing precision,
routing recall, semantic activation reliability, or model-level routing consistency.

> **Automatic routing is architecturally configured and locally validated, but semantic routing
> precision and recall remain unverified unless a real runtime evaluation is explicitly
> authorized.**

The eval cases live in `plugins/*/evals/` and are committed but **not executed**.
`docs/routing-tests.md` records them with expectations filled in and results blank.

`validate.sh` includes a **static trigger-coverage matrix**: for each scenario, which terms appear
in which description, flagging scenarios no skill covers and scenarios five skills compete for.
It catches orphaned and overlapping descriptions early. **It is a lexical proxy, not proof of
routing** — the real matcher is semantic. It is never presented as evidence that routing works.

No evidence is manufactured. Static trigger matching is not proof that Claude will activate a
skill.

---

## Changing this architecture

Adding a capability goes through [`capability-policy.md`](capability-policy.md).

Changing the architecture itself — scopes, plugin boundaries, the no-router principle, the cost
policy — requires updating this document in the same commit as the change, and re-running
`scripts/validate.sh` and `scripts/measure.sh` with the new numbers recorded.

The failure mode this repository is recovering from is accretion: ten commits that only ever
added, until four skills each claimed to be the top-level orchestrator. **Consolidating is part of
the work, not a cleanup task for later.**
