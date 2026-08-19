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

### Domain plugins @ 0.1.0 — measured

Measured the same way, each installed at `local` scope. All are **PROJECT scope**: none
is resident unless a project installs it.

| Plugin | Always-on | Components (always-on / on-invoke) |
|---|---:|---|
| `quality` | **~246 tok** | `postflight-audit` ~210 / ~1.4k · `/postflight` ~30 / ~520 |
| `engineering` | **~478 tok** | `python-dev-discipline` ~240 / ~2.1k · `deep-module-architecture` ~240 / ~1.4k |
| `frontend` | **~481 tok** | `diseno-web-estrategico` ~250 / ~2.9k · `ui-ux-review` ~240 / ~1.6k |
| `research` | **~426 tok** | `deep-research` ~200 / ~1.3k · `decision-comparison` ~220 / ~1.2k |
| `architecture` | **~293 tok** | `icm-architect` ~290 / ~3.5k |
| `finance` | **~233 tok** | `news-prioritization` ~230 / ~2.4k |

**Everything at user scope would cost ~2,797 ambient tokens** — more than four times the
core alone. That figure is the entire argument for scoping by project: a repository with
no Python, no UI, and no market exposure pays 640, not 2,797.

`icm-architect` at ~290 is the most expensive single description in the library, which is
why it stays at PROJECT scope rather than being promoted. The audit predicted ~300 for
it; the measurement confirms it.

### The `quality` promotion decision — decided by the number

The plan left this open deliberately: build `postflight-audit` in its own plugin, measure,
then decide whether it is promoted to USER scope.

**Measured: `quality` is ~246 ambient tokens. Core + quality = ~886 against a ~600
target — 48% over.**

**It is not promoted.** The core is already 40 tokens over target with a documented
reason; taking it to 886 would not be an overshoot, it would be a different budget quietly
adopted. `postflight-audit` is close to universal in *usefulness*, but universality is not
the test — cost against the ambient budget is, and that is what the measurement decides.

The practical cost of this call is close to zero: `scripts/init-project.sh` installs
`quality` in every project by default, so it is present wherever work gets finished.
Anyone who wants it resident everywhere can promote it in one command:

```bash
claude plugin install quality@ai-engineering-os --scope user
```

That is a choice worth **+246 ambient tokens in every session, forever**, and it should be
made with the number visible.

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
| Components enumerate | `claude plugin details core-discipline` | ✅ 3 skills, 1 agent, 0 hooks, 0 MCP, 0 LSP — the CLI counts the `/preflight` command among skills, so "3" is 2 skills + 1 command |
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

From `scripts/validate.sh`. For each scenario it reports **how many distinct scenario
terms each description claims**, not merely which descriptions contain one.

| Scenario | Matched (term count) | Verdict |
|---|---|---|
| `trivial` | *(none)* | ✅ **excluded** by `preflight-planning`, `postflight-audit` |
| `python` | python-dev-discipline **(5)**, icm-architect (1), preflight-planning (1), deep-module-architecture (1) | ✅ |
| `web-api` | icm-architect (1), preflight-planning (1), diseno-web-estrategico (1) | ✅ nobody claims it strongly |
| `research` | deep-research **(5)** | ✅ |
| `comparison` | decision-comparison **(4)** | ✅ |
| `ui` | ui-ux-review **(5)**, diseno-web-estrategico (1) | ✅ |
| `architecture-audit` | deep-module-architecture **(6)**, icm-architect (2), + four at (1) | ✅ |
| `large-project` | icm-architect **(3)** | ✅ |
| `document` | *(none)* | ✅ negative assertion holds |
| `email` | *(none)* | ✅ negative assertion holds |
| `video` | *(none)* | ✅ negative assertion holds |
| `multi-agent` | preflight-planning **(2)**, postflight-audit (1), python-dev-discipline (1) | ✅ both expected skills present |

**0 errors, 0 warnings. Every scenario is covered, and every expected skill wins its own
scenario outright.**

**This is a lexical proxy. It is not evidence that routing works.** The real matcher is
semantic; this one counts words. It earns its place by catching two failures cheaply: a
scenario no description covers (guaranteed recall failure) and a scenario several
descriptions claim with equal strength (predictable precision failure).

### Six defects this matrix found — in itself

Every one was fixed in the tool, never papered over. **Five of the six made the tool
report the opposite of the truth**, which is worse than reporting nothing.

1. `trivial` matched inside *non-trivial*. Matching is now word-bounded.
2. Terms in a skill's **do NOT use** clause counted as claims. The matcher now splits
   each description at its exclusion clause; terms found there mean the skill disclaims
   the scenario, and are reported as such.
3. **Membership was scored as competition.** A skill matching one generic verb
   (*refactor*) ranked equal to one matching six, so `python` and `architecture-audit`
   were flagged as precision failures when they are clean 5-to-1 and 6-to-2 separations.
   Scoring is now by distinct terms matched, and a rival needs at least two before the
   tool calls it a risk.
4. **The exclusion clause was invisible in Spanish.** `NO la uses para bugs de backend`
   never matched a pattern written as `no uses`, because Spanish puts a clitic between
   them. Every term the skill explicitly disclaimed counted as a positive claim.
5. **The same clause was also wrapped mid-phrase by the YAML folded scalar**, so even the
   English patterns missed it whenever the line broke in the wrong place. Descriptions are
   now whitespace-normalised before splitting.
6. **A scenario could only expect one skill.** `12-multi-agent` reads *"Plan it out, then
   check the work when it's done"* — two requests in one sentence, correctly answered by
   two skills. The schema forced one, so the second was reported as competition. `expect`
   now accepts a list. The same scenario's `terms` also listed *review* and *audit*, which
   appear nowhere in its prompt and are common vocabulary across the library — generic
   terms manufacturing a warning out of nothing. Terms now come from the prompt.

Defects 4 and 5 are the ones worth remembering: **a validator that silently inverts its
own signal is worse than no validator**, and they only surfaced because a Spanish-language
skill met a checker whose patterns had been written against English ones.

### The matrix is verified non-vacuous

A checker that always passes is decoration. Both failure branches were forced and both
fired, then reverted:

| Injected fault | Result |
|---|---|
| Scenario expects a skill that does not exist | `GAP`, reported as not-yet-built |
| Scenario expects a skill whose description contains none of its terms | `WARN` — likely recall failure |
| A rival matches more strongly than the expected skill | `WARN` — precision risk |
| Registry points at a moved path, or names a renamed skill | 3 errors, non-zero exit |
| Two capability files with identical content | 1 duplicate error |

## 3b. Cold-project installation — tested

`scripts/init-project.sh`, run against throwaway directories. Free, local, repeatable.

| Case | Expected | Result |
|---|---|---|
| `--dry-run` on an empty project | prints the plan, writes nothing | ✅ directory still empty afterwards |
| Empty project | `core-discipline` + `quality` only | ✅ |
| `pyproject.toml` present | + `engineering` | ✅ |
| `package.json` present | + `frontend` | ✅ |
| `pyproject.toml` + `src/App.tsx` | + both | ✅ |
| First real run | installs, writes `.claude/settings.json` | ✅ 2 installed |
| **Second identical run** | **changes nothing** | ✅ md5 identical, reports 0 installed / 2 already present |
| Pre-existing unrelated `settings.json` | warns, then merges | ✅ `permissions.allow` preserved verbatim |
| `--only <unknown-plugin>` | clear error, non-zero exit | ✅ exit 1, lists valid names |
| `--scope <invalid>` | clear error before any change | ✅ exit 1 |
| Non-existent target directory | clear error | ✅ exit 1 |
| Unknown option | clear error | ✅ exit 1 |

`research`, `architecture`, and `finance` are deliberately **not** auto-detected. Nothing
on disk indicates that a project does research or follows markets, and guessing installs
ambient cost the project may never use. They are opt-in via `--only`.

### The defect this test found

The first idempotency run **passed on outcome and failed on honesty**: `settings.json` was
byte-identical across runs, but the script reported *"installed: core-discipline, quality,
engineering"* the second time — it had installed nothing.

The cause was reading `claude plugin list` and matching plugin names against its output.
That output formats entries as `> name@marketplace`, so the pattern never matched and
every plugin looked absent. Installation detection now reads the settings file for the
requested scope, which is what actually records the state.

**A script that reports work it did not do is the same class of failure as a validator
that reports a check it did not run.** The outcome being safe is not the standard.

### What this does not establish

The install test proves the capabilities are **installed and enumerable** in a cold
project. It does not prove a cold Claude will **choose** the right one — that is the
routing question, and it falls under §4.

---

## 4. Semantic routing — NOT MEASURED

> **Automatic routing is architecturally configured and locally validated, but semantic
> routing precision and recall remain unverified unless a real runtime evaluation is
> explicitly authorized.**

### Why

`claude plugin eval` runs real agents and LLM graders, which incurs monetary cost. The
project's cost policy forbids operations that create additional billing. The cases are
therefore **written and committed but never executed here**.

### The cases, and where they had to move

Thirteen scenarios, each a directory with `prompt.md` and one grader per assertion. Five
are negative assertions. `01-trivial` is the most important: a library that fires on
everything has perfect recall and useless precision, and that failure is invisible unless
tested for directly.

**They were all in `core-discipline/evals/` and that was a defect.** Under
`--ablation with-without`, the *with* and *without* arms differ only by the plugin being
evaluated. Nine cases asserted that skills from `engineering`, `architecture`, `frontend`
and `research` fired — those skills' behaviour is identical in both arms, so a `with-only`
grader would have produced **no signal while looking like a passing test**. Spending money
on that suite would not have answered the routing question.

Each case now lives with the plugin whose skills it tests, which is also what
`capability-policy.md` said to do all along:

| Plugin | Cases |
|---|---|
| `core-discipline` | `01-trivial`, `02-web-api`, `03-document`, `04-email`, `05-video`, `06-multi-agent` |
| `quality` | `01-completion-gate` — newly written; `quality` had no cases at all |
| `engineering` | `01-python`, `02-architecture-audit` |
| `architecture` | `01-large-project` |
| `frontend` | `01-ui` |
| `research` | `01-research`, `02-comparison` |

Each plugin is evaluated separately. One grader remains deliberately cross-plugin —
`engineering/evals/02-architecture-audit` asserts that `icm-architect` does *not* fire —
and is only meaningful with both plugins installed.

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
| `12-multi-agent` | preflight-planning + postflight-audit | justified N | — | — | NOT EXECUTED |

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
| Skills, agents, commands enumerate | ✅ as the CLI counts them: 3 skills (2 + the `/preflight` command), 1 agent |
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

- **Semantic routing.** Still the one thing no local check reaches. See §4.
- **Double-loading against account-synced skills.** Five files in this repo are still
  byte-identical to skills synced on the account (`audit-2026-08.md` §4.1). Until
  those account copies are retired through the claude.ai UI, the savings from this
  restructuring are partly cancelled. `scripts/validate.sh` warns when it detects the
  overlap.
