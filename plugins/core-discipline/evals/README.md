# Routing eval cases — defined, NOT executed

Twelve scenarios covering what this library should and should not activate on.
Each case is a directory: `prompt.md` plus one grader per assertion in `graders/`.

## Status: NOT EXECUTED — cost prohibited

`claude plugin eval` runs real agents and LLM graders, which incurs monetary cost.
The cost policy for this project (see [`../../../docs/architecture.md`](../../../docs/architecture.md))
forbids any operation that creates additional billing, so these cases are written and
committed but never run here.

**To run them yourself**, when you decide to spend:

```bash
claude plugin eval ./plugins/core-discipline \
  --ablation with-without \
  --no-publish \
  --max-cost-usd <your cap>
```

`--no-publish` is not optional. The default publishes the HTML report to claude.ai;
this repository never sends its contents to an external service without an explicit
decision to do so.

Record results in [`../../../docs/routing-tests.md`](../../../docs/routing-tests.md),
which already holds the expectations with the actual columns blank.

## What these cases test

Under `--ablation with-without`, each case runs with and without the plugin. Graders
marked `with-only` — notably `tool_used: Skill` — indicate the plugin actually fired,
which is the routing question.

| Case | Asserts |
|---|---|
| `01-trivial` | **negative** — a three-site rename must not summon planning machinery or agents |
| `02-python` | `python-dev-discipline` fires; planning depth stays proportionate |
| `03-web-api` | `preflight-planning` fires; scope stated; no speculative fan-out |
| `04-research` | `deep-research` fires; source tiers; a stopping criterion exists |
| `05-comparison` | `decision-comparison` fires; criteria precede the recommendation |
| `06-ui` | `ui-ux-review` fires; built-in design capabilities are not reimplemented |
| `07-architecture-audit` | `deep-module-architecture` fires; **`icm-architect` does not** |
| `08-large-project` | `icm-architect` fires; structure matches actual recurrence |
| `09-document` | **negative** — built-ins handle it; no repo skill competes |
| `10-email` | **negative** — official connector or a plain report of its absence |
| `11-video` | missing `ffmpeg` is reported, never faked |
| `12-multi-agent` | agent count is justified; review is adversarial with real findings |

Five of the twelve are negative assertions. **`01-trivial` is the most important case
in the suite** — a library that fires on everything has perfect recall and useless
precision, and that failure is invisible unless you test for it directly.

## Caveat on the case format

The CLI accepts `case.yaml` or `prompt.md` + `graders/*.md`. These use the second
form because its structure is self-evident from `claude plugin eval --help`; the
`case.yaml` field schema is not in the published documentation, and guessing at it
would have shipped twelve files that may not parse. If you run these and the format
needs adjusting, the prompts and assertions carry over unchanged.
