# Security tools

## Start with the built-in

Claude Code ships **`/security-review`**. It is maintained by Anthropic, it costs nothing
extra, and it is what `postflight-audit` invokes at `full` depth.

**This is why there is no `security-auditor` agent in this library.** Writing one would
duplicate a maintained built-in — the exact failure the capability policy exists to
prevent. It stays in the registry's `deferred` list with that reason recorded, and it gets
built only if the built-in is shown to be insufficient, with the evidence written down
first.

## When static analysis earns its place

`/security-review` reads the diff. It does not do interprocedural dataflow across a whole
codebase. For that:

| Tool | Notes |
|---|---|
| **Semgrep** | Rule-based, fast, large community ruleset. Runs locally |
| **CodeQL** | Query-based dataflow analysis. Heavier, deeper, GitHub-integrated |

`trailofbits/skills` provides skills built on these. Trail of Bits is a reputable security
firm and the skills are CC-BY-SA licensed, so they are a genuine option — but they
**require CodeQL or Semgrep installed**, and neither is present here.

**They are documented, not installed.** A skill that cannot run is ambient cost with no
capability behind it. If you install the tooling and want the skills, they go in a new
`security` plugin, at project scope, through the gate in `docs/adding-capabilities.md`.

## What is deliberately not here

No secret scanning skill — `mcp__github__run_secret_scanning` exists and GitHub does this
server-side. No dependency-audit skill — `npm audit`, `pip-audit`, and Dependabot already
do it, and none of them needs a skill wrapper to be run.

## The rule that matters

**Never invent, request, or hard-code a credential.** If a capability needs one, document
what the user must configure and stop there. No skill in this library reads a secret, and
none should. Before installing any external security tool, inspect its source, its install
script, its network access, and its maintainer — a tool that audits your code has read
access to all of it.
