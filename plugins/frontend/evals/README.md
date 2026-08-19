# Routing eval cases — `frontend`

## Status: NOT EXECUTED — cost prohibited

`claude plugin eval` runs real agents and LLM graders, which costs money. This project's
cost policy forbids operations that create additional billing, so these cases are written
and committed but never run here. See
[`../../core-discipline/evals/README.md`](../../core-discipline/evals/README.md) for the
full explanation and the exact command.

## Cases

These test interface review. They live here rather than in `core-discipline` because
`--ablation with-without` only toggles the plugin being evaluated: a grader asserting a
`frontend` skill fired would produce identical results in both arms if it sat in another
plugin's suite — no signal, dressed as a passing test.

01-ui — ui-ux-review fires and the built-in dataviz and artifact-design skills are not reimplemented

```bash
claude plugin eval ./plugins/frontend --ablation with-without --no-publish --max-cost-usd <cap>
```
