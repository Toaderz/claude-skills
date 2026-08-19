# Routing eval cases — defined, NOT executed

## Status: NOT EXECUTED — cost prohibited

`claude plugin eval` runs real agents and LLM graders, which incurs monetary cost. The
cost policy for this project (see [`../../../docs/architecture.md`](../../../docs/architecture.md))
forbids any operation that creates additional billing, so these cases are written and
committed but never run here.

**Each plugin holds the cases that test its own skills.** This matters more than tidiness:
under `--ablation with-without`, the *with* and *without* arms differ only by the plugin
being evaluated. A grader asserting that `python-dev-discipline` fired, sitting in
`core-discipline`'s suite, would behave identically in both arms — it would produce no
signal at all while looking like a passing test.

| Plugin | Cases |
|---|---|
| `core-discipline` | `01-trivial`, `02-web-api`, `03-document`, `04-email`, `05-video`, `06-multi-agent` |
| `quality` | `01-completion-gate` |
| `engineering` | `01-python`, `02-architecture-audit` |
| `architecture` | `01-large-project` |
| `frontend` | `01-ui` |
| `research` | `01-research`, `02-comparison` |

**To run them yourself**, when you decide to spend — one plugin at a time:

```bash
claude plugin eval ./plugins/core-discipline \
  --ablation with-without \
  --no-publish \
  --max-cost-usd <your cap>
```

`--no-publish` is not optional. The default publishes the HTML report to claude.ai; this
repository never sends its contents to an external service without an explicit decision.

Record results in [`../../../docs/routing-tests.md`](../../../docs/routing-tests.md),
which holds the expectations with the actual columns blank.

## The cases in this plugin

| Case | Asserts |
|---|---|
| `01-trivial` | **negative** — a three-site rename must not summon planning machinery or agents |
| `02-web-api` | `preflight-planning` fires; scope stated; no speculative fan-out |
| `03-document` | **negative** — built-ins handle it; no repo skill competes |
| `04-email` | **negative** — official connector or a plain report of its absence |
| `05-video` | missing `ffmpeg` is reported, never faked |
| `06-multi-agent` | agent count is justified; review is adversarial with real findings |

Four of the six are negative assertions. **`01-trivial` is the most important case in the
suite** — a library that fires on everything has perfect recall and useless precision, and
that failure is invisible unless you test for it directly.

## Caveat on the case format

The CLI accepts `case.yaml` or `prompt.md` + `graders/*.md`. These use the second form
because its structure is self-evident from `claude plugin eval --help`; the `case.yaml`
field schema is not in the published documentation, and guessing at it would have shipped
files that may not parse. If you run these and the format needs adjusting, the prompts and
assertions carry over unchanged.

## A cross-plugin caveat

`engineering/evals/02-architecture-audit` includes a grader asserting that `icm-architect`
does **not** fire. That skill ships in `architecture`, so the assertion is only meaningful
when both plugins are installed. Run it that way or read that one grader as inconclusive.
