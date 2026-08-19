# Routing eval cases — `research`

## Status: NOT EXECUTED — cost prohibited

`claude plugin eval` runs real agents and LLM graders, which costs money. This project's
cost policy forbids operations that create additional billing, so these cases are written
and committed but never run here. See
[`../../core-discipline/evals/README.md`](../../core-discipline/evals/README.md) for the
full explanation and the exact command.

## Cases

These test research and decisions. They live here rather than in `core-discipline` because
`--ablation with-without` only toggles the plugin being evaluated: a grader asserting a
`research` skill fired would produce identical results in both arms if it sat in another
plugin's suite — no signal, dressed as a passing test.

01-research — deep-research fires with source tiers and a stopping criterion · 02-comparison — decision-comparison fires and criteria precede the recommendation

```bash
claude plugin eval ./plugins/research --ablation with-without --no-publish --max-cost-usd <cap>
```
