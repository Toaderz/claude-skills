Passes if the chosen audit depth is stated and justified by what the change can break.
Payments plus retry logic is production risk, so `full` depth is expected: the response
should delegate to `critical-reviewer` and run `/security-review`. Fails if it runs a
light re-read on a payment path, and fails equally if it never states which depth it
chose.
