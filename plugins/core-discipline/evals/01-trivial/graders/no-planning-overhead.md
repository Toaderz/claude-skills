Fails if the response produces a formal plan, a pre-mortem, a risk analysis, or a
scope/constraints breakdown before making the edit.

This is the most important case in the suite, and it is a negative assertion. A
three-site rename is exactly what `preflight-planning`'s exclusion clause is for.
Planning machinery firing here means the gate does not work.
