# GitHub

## Use the MCP tools, not `gh`

In a Claude Code remote session there is **no `gh` CLI and no direct API access**. All
GitHub work goes through `mcp__github__*` tools, loaded on demand.

This is why `deep-module-architecture` writes its RFC with `mcp__github__issue_write`
rather than `gh issue create` — the original skill used `gh`, and it would have failed
silently every time.

**When the tools are unavailable, degrade visibly.** That skill outputs the RFC as
markdown and says the GitHub tools are missing. It does not shell out to a command that
is not there.

## The permission ceiling

**The connected GitHub App has no Administration permission.**
`mcp__github__create_repository` fails with `403 Resource not accessible by integration`,
for personal accounts and organisations alike.

Files, branches, pull requests, issues, and reviews in already-authorised repositories
work normally. **Creating a repository does not.** A new repository has to be created by
hand and then attached with `add_repo`.

Repository access is scoped per session. If a repository exists but is not enabled for the
workspace, an administrator grants access in the Claude GitHub settings; you reconnect
your own authorisation under claude.ai Settings → Connectors.

## Official plugins

`anthropics/claude-plugins-official` is registered automatically and carries integrations
for GitHub, Linear, Sentry, and Figma with their MCP servers configured. **Prefer these
over community equivalents** — same function, first-party maintenance.

```bash
claude plugin marketplace list      # it is already there
```

This library does not vendor or duplicate them.
