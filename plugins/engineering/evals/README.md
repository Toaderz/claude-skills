# Routing eval cases — `engineering`

## Status: NOT EXECUTED — cost prohibited

`claude plugin eval` runs real agents and LLM graders, which costs money. This project's
cost policy forbids operations that create additional billing, so these cases are written
and committed but never run here. See
[`../../core-discipline/evals/README.md`](../../core-discipline/evals/README.md) for the
full explanation and the exact command.

## Cases

These test Python discipline and module architecture. They live here rather than in `core-discipline` because
`--ablation with-without` only toggles the plugin being evaluated: a grader asserting a
`engineering` skill fired would produce identical results in both arms if it sat in another
plugin's suite — no signal, dressed as a passing test.

01-python — python-dev-discipline fires and planning stays proportionate · 02-architecture-audit — deep-module-architecture fires and icm-architect does not

```bash
claude plugin eval ./plugins/engineering --ablation with-without --no-publish --max-cost-usd <cap>
```
