# Adding a capability

The gate every addition passes, and the form the justification takes.

Companion documents: [`capability-policy.md`](capability-policy.md) for the full policy,
[`architecture.md`](architecture.md) for the structural contract.

---

## 1. The gate: do not duplicate

Ask in this order and **stop at the first yes**:

```
Is it a Claude Code built-in?          → use it
Is it an official Anthropic skill?     → use it
Is there an official MCP or connector? → evaluate it
Is there a local CLI that does it?     → use it
Does it genuinely need a new Skill?    → only now, build it
```

Already native — **never rebuild these**:

| Need | Use |
|---|---|
| Word, PDF, PowerPoint, Excel | `docx`, `pdf`, `pptx`, `xlsx` |
| Line-by-line code review | `/code-review` |
| Security review | `/security-review` |
| Charts, dashboards | `dataviz` |
| Standalone visual artifacts | `artifact-design` |
| Authoring or measuring a skill | `skill-creator` |
| Web search and fetch | `WebSearch`, `WebFetch` |
| Delegating isolated work | the `Agent` tool |
| Email | the official claude.ai connector — **not a community MCP** |

Duplicating any of these is pure cost: ambient tokens spent, a routing rival created, and
a second thing to maintain that upstream already maintains better.

## 2. Pick the right type

| Need | Type |
|---|---|
| A method, discipline, or body of knowledge applied to work | **Skill** |
| Work that benefits from an isolated context and restricted tools | **Agent** |
| An explicit, repeatable entry point the user types | **Command** |
| Access to an external system | **MCP or connector** — document it, do not install it by default |

**The agent test.** All must hold, or make it a skill:

1. The work is genuinely separable.
2. **Context isolation helps rather than hurts.** An agent that did not see what you just
   built writes worse tests than you do — this is why `test-engineer` stays deferred.
3. Restricted tools are part of the point (read-only means it cannot "fix it and call it
   fine").
4. It has one mission, a bounded scope, and a stopping condition.
5. It does not duplicate a built-in — this is why `security-auditor` stays deferred.
6. The benefit is describable before it is built.

**Never add an agent because agents exist.** One is the default; the library ships one.

## 3. Write the description

The description is the only thing loaded until the skill fires, so it *is* the routing
decision. Get it wrong and the body never runs.

- **Say what it does, then when to use it, then when NOT to.** The exclusion clause is
  what buys precision; `scripts/validate.sh` reads it and reports terms found there as
  disclaimed rather than claimed.
- **Include literal trigger phrases in English and Spanish** — the words a user actually
  types, not a topic summary.
- **Discriminate.** If two skills would match the same request equally, one of them is
  wrong. The coverage matrix scores by how many scenario terms each description claims,
  so a rival tying the expected skill is reported.
- **Stay under 1,024 characters**, and remember every character is resident forever in
  the sessions where the plugin is installed. Redundant synonyms cost tokens and buy
  nothing: trimming them took the core from ~795 to ~640 with an identical matrix.

## 4. Pick the plugin — the plugin is the scope

A plugin is the unit of installation. **Skills inside one cannot be scoped separately**,
so choosing the plugin *is* choosing the scope.

| Plugin | Scope | For |
|---|---|---|
| `core-discipline` | USER | universal in any project |
| `quality`, `engineering`, `architecture`, `frontend`, `research`, `finance` | PROJECT | depends on the kind of work |

Adding to `core-discipline` means paying its ambient cost in **every session forever**.
Measure before proposing it: `scripts/measure.sh`.

## 5. Justify it in writing

The pull request states:

1. **Which built-in alternative was considered, and why it does not cover this.** Not
   optional — this is the whole gate.
2. **The type chosen and why** — and for an agent, the six conditions above, answered.
3. **The plugin and therefore the scope**, with the measured ambient cost if it lands in
   `core-discipline`.
4. **What it replaces**, if anything. A new capability that overlaps an existing one
   should absorb it, not race it.
5. **The scenario it must win** in `scripts/lib/scenarios.json`, and the scenarios it
   must *not* claim.

## 6. Validate

```bash
scripts/validate.sh    # manifests, links, duplicates, registry, coverage matrix
scripts/measure.sh     # real ambient cost, per plugin
```

Then add the capability to `registry/registry.json` — name, type, plugin, path, purpose,
triggers, exclusions, dependencies, scope, cost, what it replaces.

**The registry is inventory for humans, not a router.** Claude never reads it per
request; native description matching does the routing. It exists for maintenance,
auditing, and knowing what is already here before adding something that overlaps it.

---

## On third-party skill ecosystems

There is an ecosystem outside Anthropic's — `npx skills` and https://skills.sh among
them. This repository does not wrap it in a skill: **"how to install things" is
documentation you read once, not behaviour worth ambient tokens in every session**, and
Claude Code's own `/plugin marketplace` is the supported path.

Before installing anything external, inspect it: source and maintainer, requested
permissions, install scripts, dependencies, network and filesystem access, credential
requirements, obfuscated code. **A plugin that installs a `SessionStart` hook can
restructure how every session behaves** — that is the reason `obra/superpowers` was
evaluated and rejected as a base, despite its popularity. Stars are not curation.
