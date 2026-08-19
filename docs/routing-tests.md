# Routing and context measurements

Everything measured about this library, and everything not measured, stated as such.

Companion documents: [`architecture.md`](architecture.md) for the design and the cost
policy, [`audit-2026-08.md`](audit-2026-08.md) for the pre-restructure baseline.

---

## 1. Context footprint — measured

`scripts/measure.sh`, wrapping `claude plugin details`. This is a static local
computation and costs nothing.

**Target: ≤600 ambient tokens for the USER-scope core.** A target, not a runtime limit.

### `core-discipline` @ 0.1.0

| Measurement | Always-on | On-invoke |
|---|---:|---:|
| **Total** | **~640 tok** | — |
| `preflight-planning` | ~230 | ~3.1k |
| `project-memory` | ~230 | ~2.4k |
| `critical-reviewer` | ~150 | ~1.1k |
| `/preflight` | ~40 | ~460 |

The CLI labels these projections and notes they may differ from actual usage. Reported
as returned, unadjusted.

### Domain plugins @ 0.1.0 — measured after the migration

Measured the same way, with each plugin installed at `local` scope. These are **PROJECT
scope**: none of them is resident unless a project installs it.

| Plugin | Always-on | Components |
|---|---:|---|
| `engineering` | **~478 tok** | `python-dev-discipline` ~240 (~2.1k on-invoke) · `deep-module-architecture` ~240 (~1.4k) |
| `architecture` | **~293 tok** | `icm-architect` ~290 (~3.5k) |
| `frontend` | **~265 tok** | `diseno-web-estrategico` ~270 (~3.1k) |
| `finance` | **~233 tok** | `news-prioritization` ~230 (~2.3k) |

**Everything installed at user scope would cost ~1,909 ambient tokens** — three times the
core alone. That number is the whole argument for scoping by project: a repository with no
Python, no UI, and no market exposure pays 640, not 1,909.

`icm-architect` at ~290 is the single most expensive description in the library, which is
why it stays in `architecture` at PROJECT scope rather than being promoted. The audit
predicted ~300 for it; the measurement confirms it.

### What happened when it came in over target

First measurement: **~795 tokens**, 33% over. Applying the procedure from
`architecture.md` — measure, find the highest-cost/lowest-value item, reduce metadata
or move scope, re-measure:

The cost was concentrated in description length, and the descriptions carried
redundant trigger synonyms: nine English verbs plus nine Spanish ones for
`preflight-planning`, several near-identical phrasings for `project-memory`. Cutting
the redundant synonyms took the core to **~640 tokens** with **no change to the static
trigger-coverage matrix** — same scenarios matched, same scenarios excluded, before
and after. That is metadata reduction without signal loss.

### Why it stops at 640 and not 600

**It does not close the last 40 tokens, and that is a deliberate call.** The remaining
description text is discriminative triggers and exclusion clauses. Cutting further
would mean either removing trigger phrases that buy recall or deleting a capability
outright, and 640 tokens for planning discipline, durable memory, adversarial review,
and an explicit entry point is good value.

`architecture.md` states the governing principle: the goal is minimum *useful* context,
not minimum tokens at any cost, and routing quality is not sacrificed to satisfy an
arbitrary figure. Reporting 640 against a 600 target is the honest outcome. Adjusting
the target to 640 after the fact, or gutting a capability to reach 600, would both be
worse.

---

## 2. Installation mechanics — verified

Run against the real CLI (2.1.235). Free, local, reproducible.

| Check | Command | Result |
|---|---|---|
| Marketplace resolves | `claude plugin marketplace add ./ --scope local` | ✅ registered as `ai-engineering-os` |
| Marketplace listed | `claude plugin marketplace list` | ✅ resolves as `Source: Directory` at the repo root |
| Plugin installs | `claude plugin install core-discipline@ai-engineering-os --scope local` | ✅ scope `local` |
| Plugin enabled | `claude plugin list` | ✅ `0.1.0`, enabled |
| Components enumerate | `claude plugin details core-discipline` | ✅ 3 skills, 1 agent, 0 hooks, 0 MCP, 0 LSP |
| Manifests valid | `claude plugin validate ./` and `--strict` per plugin | ✅ both pass |
| Repo lint | `scripts/validate.sh` | ✅ 0 errors, 0 warnings |

Two defects this step found and fixed:

- **`marketplace.json` rejected `metadata.pluginRoot`-relative sources.**
  `"source": "core-discipline"` failed with `plugins.0.source: Invalid input`; the
  explicit `"./plugins/core-discipline"` validates. Caught by the validator on its
  very first run.
- **Installing wrote `.claude/settings.local.json` containing this machine's absolute
  path.** A global gitignore happened to hide it here, so on any machine without that
  global rule it would have been committed. The repo now has its own `.gitignore`.

Note: `claude plugin details` reads the plugin directory live, so edits are reflected
without reinstalling. `claude plugin update` does not apply to a directory-sourced
plugin and reports it as not found — expected, not a defect.

---

## 3. Static trigger-coverage matrix — a proxy, not proof

From `scripts/validate.sh`. For each scenario it now reports **how many distinct scenario
terms each description claims**, not merely which descriptions contain one.

| Scenario | Matched (term count) | Verdict |
|---|---|---|
| `trivial` | *(none)* | ✅ **explicitly excluded** by `preflight-planning` |
| `python` | python-dev-discipline **(5)**, icm-architect (1), preflight-planning (1), deep-module-architecture (1) | ✅ clean separation |
| `web-api` | icm-architect (1), preflight-planning (1), diseno-web-estrategico (1) | ✅ nobody claims it strongly |
| `research` | *(none)* | ⏳ `deep-research` not built yet |
| `comparison` | *(none)* | ⏳ `decision-comparison` not built yet |
| `ui` | diseno-web-estrategico (1) | ⏳ `ui-ux-review` not built yet |
| `architecture-audit` | deep-module-architecture **(6)**, icm-architect (2), preflight-planning (1), python-dev-discipline (1) | ✅ clean separation |
| `large-project` | icm-architect **(3)** | ✅ |
| `document` | *(none)* | ✅ negative assertion holds |
| `email` | *(none)* | ✅ negative assertion holds |
| `video` | *(none)* | ✅ negative assertion holds |
| `multi-agent` | preflight-planning (2), deep-module-architecture (2), news-prioritization (1), diseno-web-estrategico (1) | ⚠️ **tie — see below** |

**This is a lexical proxy. It is not evidence that routing works.** The real matcher is
semantic; this one counts words. It earns its place by catching two failures cheaply: a
scenario no description covers (guaranteed recall failure) and a scenario several
descriptions claim with equal strength (predictable precision failure).

### The one open warning

`multi-agent` is a tie at two terms: `preflight-planning` claims *plan* and *planifica*,
`deep-module-architecture` claims *review* and *revisa*. Semantically these are not
competing — the second only ever says "architecture review" and "revisa la arquitectura" —
but the proxy scores unigrams, so a bigram whose first word is generic reads as a claim.

**The warning is left standing rather than tuned away.** Removing "architecture review"
from a description to silence a word-counter would trade real recall for a green line.

### Four defects this matrix has now found in itself

Every one was fixed in the tool, not papered over:

1. `trivial` matched inside *non-trivial*. Matching is now word-bounded.
2. Terms occurring in a skill's **do NOT use** clause counted as claims. The matcher now
   splits each description at its exclusion clause; terms found there mean the skill
   disclaims the scenario, and are reported as such.
3. **Membership was scored as competition.** A skill matching one generic verb
   (*refactor*) ranked equal to one matching six, so `python` and `architecture-audit`
   were flagged as precision failures when they are in fact clean 5-to-1 and 6-to-2
   separations. Scoring is now by distinct terms matched, and a rival must claim at least
   two before the tool calls it a risk.
4. **The exclusion clause was missed in Spanish.** `NO la uses para bugs de backend` did
   not match a pattern written as `no uses`, because Spanish puts a clitic between them —
   and the clause was also wrapped mid-phrase by the YAML folded scalar. Every term the
   skill explicitly disclaimed was being counted as a positive claim, which is exactly
   backwards. Descriptions are now whitespace-normalised before splitting, and the
   pattern covers the clitic forms.

Defect 4 is the one worth remembering: **a validator that silently inverts its own signal
is worse than no validator**, and it only surfaced because a Spanish-language skill was
migrated into a checker whose patterns had been written against English ones.

## 4. Semantic routing — NOT MEASURED

> **Automatic routing is architecturally configured and locally validated, but semantic
> routing precision and recall remain unverified unless a real runtime evaluation is
> explicitly authorized.**

### Why

`claude plugin eval` runs real agents and LLM graders, which incurs monetary cost. The
project's cost policy forbids operations that create additional billing. The cases are
therefore **written and committed but never executed here**.

### The cases

Twelve scenarios in [`../plugins/core-discipline/evals/`](../plugins/core-discipline/evals/),
each a directory with `prompt.md` and one grader per assertion. Five are negative
assertions. `01-trivial` is the most important: a library that fires on everything has
perfect recall and useless precision, and that failure is invisible unless tested for
directly.

| Case | Expected skills | Expected agents | Actual skills | Actual agents | Result |
|---|---|---|---|---|---|
| `01-trivial` | **none** | **0** | — | — | NOT EXECUTED |
| `02-python` | python-dev-discipline | 0 | — | — | NOT EXECUTED |
| `03-web-api` | preflight-planning | 0–1 | — | — | NOT EXECUTED |
| `04-research` | deep-research | 0–1 | — | — | NOT EXECUTED |
| `05-comparison` | decision-comparison | 0 | — | — | NOT EXECUTED |
| `06-ui` | ui-ux-review | 0 | — | — | NOT EXECUTED |
| `07-architecture-audit` | deep-module-architecture | 0–1 | — | — | NOT EXECUTED |
| `08-large-project` | icm-architect | 0 | — | — | NOT EXECUTED |
| `09-document` | **none** (built-ins) | **0** | — | — | NOT EXECUTED |
| `10-email` | **none** (connector) | **0** | — | — | NOT EXECUTED |
| `11-video` | **none** — report missing `ffmpeg` | **0** | — | — | NOT EXECUTED |
| `12-multi-agent` | preflight-planning | justified N | — | — | NOT EXECUTED |

### To execute them

```bash
claude plugin eval ./plugins/core-discipline \
  --ablation with-without \
  --no-publish \
  --max-cost-usd <your cap>
```

`--no-publish` is required: the default publishes the report to claude.ai.

Under `--ablation with-without`, each case runs with and without the plugin, and
graders marked `with-only` (`tool_used: Skill`) indicate the plugin actually fired.

### Precision and recall

Not computed. They require the actual-activation data the runtime evaluation produces.
No estimate is substituted, and the static matrix in §3 is not offered as one.

### If routing does turn out to be wrong

Diagnose in this order before building anything:

1. weak description → 2. wrong installation scope → 3. invalid plugin structure →
4. malformed frontmatter → 5. `paths:` behavior ([#49835](https://github.com/anthropics/claude-code/issues/49835)) →
6. a current limitation of Claude Code → 7. genuinely absent functionality.

Only the last justifies building machinery. **A routing miss is not a reason to build
a router.**

---

## 5. Pilot gate

Stage A is complete when every free check passes. Status as of commit 5:

| Gate condition | Status |
|---|---|
| Marketplace resolves | ✅ |
| Plugin installs | ✅ |
| Skills, agents, commands enumerate | ✅ 3 skills, 1 agent |
| Scope behaves | ✅ verified at `local` |
| `claude plugin validate --strict` green | ✅ |
| 0 broken links | ✅ |
| 0 duplicates by hash | ✅ within `plugins/` |
| Registry consistent with disk | ✅ and verified non-vacuous — injecting a bad path and a renamed skill produced 3 errors and a non-zero exit |
| Context footprint measured and reported | ✅ **~640 tok**, over the 600 target, with the reasoning in §1 |
| Semantic routing works | ⛔ **not a gate condition** — requires an authorized runtime evaluation |

**Result: gate passed**, with the context footprint over target by 40 tokens and the
reason recorded rather than the number massaged.

### Not yet verified

- **`scripts/init-project.sh`** does not exist yet. It has nothing to install until
  the domain plugins are built, so the cold-project and idempotency test moves to
  Stage B.
- **Double-loading against account-synced skills.** Five files in this repo are still
  byte-identical to skills synced on the account (`audit-2026-08.md` §4.1). Until
  those account copies are retired through the claude.ai UI, the savings from this
  restructuring are partly cancelled. `scripts/validate.sh` warns when it detects the
  overlap.
