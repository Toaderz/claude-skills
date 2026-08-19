# Routing eval cases — `architecture`

## Status: NOT EXECUTED — cost prohibited

`claude plugin eval` runs real agents and LLM graders, which costs money. This project's
cost policy forbids operations that create additional billing, so these cases are written
and committed but never run here. See
[`../../core-discipline/evals/README.md`](../../core-discipline/evals/README.md) for the
full explanation and the exact command.

## Cases

These test ICM workspaces. They live here rather than in `core-discipline` because
`--ablation with-without` only toggles the plugin being evaluated: a grader asserting a
`architecture` skill fired would produce identical results in both arms if it sat in another
plugin's suite — no signal, dressed as a passing test.

01-large-project — icm-architect fires and the structure matches actual recurrence, not imagined stages

```bash
claude plugin eval ./plugins/architecture --ablation with-without --no-publish --max-cost-usd <cap>
```
