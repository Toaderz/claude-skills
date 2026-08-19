# Capability policy

**DO NOT DUPLICATE CAPABILITIES.**

This is the gate every proposed capability passes before it is built. It exists because the
alternative is observable: this repository once held four skills that each declared themselves the
top-level orchestrator, and an ecosystem left ungoverned drifts toward

```
research · deep-research · advanced-research · research-pro
research-agent · research-orchestrator · research-workflow
```

all solving essentially the same problem, none of them clearly the one to use.

---

## The gate

```
CAPABILITY REQUEST
        │
        ▼
Does Claude Code already do this natively? ──── YES ──▶ use the built-in
        │ NO
        ▼
Is there an official Anthropic capability? ──── YES ──▶ use it
        │ NO
        ▼
Is there an official MCP or connector? ──────── YES ──▶ evaluate it (see Security)
        │ NO
        ▼
Is there a CLI or local tool? ───────────────── YES ──▶ use it, document the dependency
        │ NO
        ▼
Do we genuinely need a Skill? ───────────────── YES ──▶ build it
        │ NO
        ▼
        don't build it
```

Every step is a real stop, not a formality. Most requests terminate before the last one.

---

## Already native — do not rebuild

Available with nothing added to this repository:

| Capability | Use instead of building |
|---|---|
| `docx` `pdf` `pptx` `xlsx` | document reading and generation |
| `/code-review` | general code review |
| `/security-review` | security review |
| `dataviz` | charts and data visualization |
| `artifact-design` | designed HTML deliverables |
| `skill-creator` | scaffolding new skills |
| `WebSearch` / `WebFetch` | web research primitives |
| the `Agent` tool | subagent orchestration |
| claude.ai connectors | Gmail and other authenticated services |

**Claude Code also already routes skills** — it preloads `name` and `description` and loads bodies
on match. Do not build a router. See [`architecture.md`](architecture.md).

---

## Choosing the right kind of thing

Not everything is a Skill.

| Need | Type | Why |
|---|---|---|
| Methodology, engineering discipline, research method, architecture, memory | **Skill** | reusable procedure the model follows in its own context |
| Adversarial review with a bounded mission and isolated context | **Agent** | isolation is the mechanism; the agent must not see the reasoning it is checking |
| An explicit, repeatable entry point | **Command** | the user wants to *invoke* it by name, not hope it triggers |
| Browser control | **MCP** | stateful protocol; documented, not installed by default (Playwright ≈13.7k tokens/request, Chrome DevTools ≈19k) |
| Email | **Connector** | official Anthropic connector; never a community MCP asking for mailbox OAuth |
| Video, audio, OCR, document conversion | **CLI + orchestrating skill** | `ffmpeg`, `whisper.cpp` and friends run locally; the skill sequences them |
| Documents, code review, security review, web search, orchestration | **built-in** | already exists |

### The agent test

Before adding an agent, all of these must hold:

1. it has a clearly defined mission;
2. there is a concrete reason it adds value over the main agent;
3. its scope is bounded;
4. its tools are the minimum sufficient set;
5. the expected benefit is measurable;
6. it has a stopping condition.

And ask specifically: **does context isolation help here, or hurt?** For adversarial review it
helps — the reviewer cannot be anchored by reasoning it never saw. For writing tests it hurts —
an agent that did not see what was just built writes worse tests than the main agent that did.

**Prefer one agent when one suffices.** Never a default fleet. Optimize for maximum useful work
per token and per tool call, not for agent count.

---

## Security review before adopting anything external

Before installing an MCP server, plugin, or CLI dependency, inspect and record:

- source and maintainer reputation
- what permissions it requests
- install scripts — read them
- transitive dependencies
- network access it performs
- filesystem access it performs
- credentials it requires
- obfuscated or minified code
- ambient token cost per request

**Never invent or request secrets unnecessarily.** If a tool needs credentials, document what the
user must configure manually — do not collect them, do not embed them, do not commit them.

**Never auto-install anything suspicious.** Popularity is not a quality signal: a 40k-star plugin
that installs a `SessionStart` hook and hijacks the development flow is a worse fit than an
unstarred one that does not.

Prefer, in order: official Anthropic → reputable named maintainer → local CLI with no network →
community. A community MCP that wants OAuth to a mailbox when an official connector exists is not
a trade-off, it is a mistake.

---

## Missing dependencies must be reported, never faked

Several capabilities depend on binaries that are **not installed** in this environment: `ffmpeg`,
`ffprobe`, `whisper`, `yt-dlp`, `pandoc`, `tesseract`, `gh`.

A skill that depends on one of these must **detect its absence and say so plainly**, naming what
the user needs to install. It must not fail silently, and it must not pretend the capability
exists. Installation instructions belong in `integrations/`.

---

## Adding a capability

1. **Walk the gate above.** Write down which built-in alternative you rejected and why.
2. **Check the registry** (`registry/registry.json`) for overlap. If something covers 60% of it,
   the answer is probably to extend that, not to add a sibling.
3. **Pick the type** from the table above.
4. **Pick the plugin**, which is the scope decision — see the scope section of
   [`architecture.md`](architecture.md). Default to PROJECT. USER scope must be earned.
5. **Write it** within the constraints below.
6. **Register it** in `registry/registry.json`.
7. **Validate**: `scripts/validate.sh` must pass clean.
8. **Measure**: if it touches `core-discipline`, run `scripts/measure.sh` and record the number.
9. **Write eval cases** in the plugin's `evals/`. They are committed, not executed — see the cost
   policy in [`architecture.md`](architecture.md).

### Constraints

| Constraint | Limit | Source |
|---|---|---|
| `name` | ≤64 chars, lowercase kebab-case, **never containing `claude` or `anthropic`** | reserved words |
| `description` | ≤1024 characters | platform spec |
| SKILL.md body | <500 lines | keeps loaded cost bounded |
| References | one level deep from SKILL.md | progressive disclosure |
| Bundled files | unlimited — they cost **zero** context until read | `references/`, `assets/`, `scripts/` |

### Writing a description that routes

The description is the entire discovery surface. It is the only text loaded at startup, and it is
where routing succeeds or fails.

- **Bilingual.** Spanish and English literal trigger phrases, since requests arrive in both.
- **Third person.** "Evaluates and ranks…", not "I evaluate…".
- **Concrete triggers.** The words a user actually types, quoted.
- **Say when NOT to activate.** This is what buys precision; without it every skill competes for
  every prompt.
- **Discriminative.** If two descriptions would match the same prompt equally well, one of them is
  wrong — or the two capabilities should be one.

Anchor on the *shape* of the request rather than the domain when the capability is genuinely
general. A comparison skill should trigger on "compare these options and recommend one," not on an
enumeration of every domain someone might compare things in.

---

## Removing a capability

Rescue before delete, in this order:

1. **Inspect** the file completely.
2. **Identify** what in it is worth keeping.
3. **Migrate** that content to its new home.
4. **Verify** the migration — the content is actually there and reachable.
5. **Only then** `git rm`.

Never delete useful information merely to make the repository smaller. Record the disposition and
the grounds, as `audit-2026-08.md` does.

---

## The question that governs all of this

> **Is there a simpler architecture that produces the same result?**

If yes, build that one instead. If a proposed capability is not worth building, say so and explain
why — including when it was explicitly requested. Twenty excellent capabilities beat a hundred
mediocre ones, and the number of files in this repository is not a measure of its quality.
