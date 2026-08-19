# Environment notes

What this library can and cannot rely on in a Claude Code remote session, and the
constraints that shape several skills.

Rescued from a dated session snapshot that had been filed as a skill. It was never a
skill — it described the environment rather than changing behaviour, so it cost ambient
tokens on every session to answer a question nobody was asking. **Documentation belongs
in `docs/`.**

Session-specific values (session id, scratchpad path, branch name, container) are
deliberately not recorded here: they change every run, and a stale value is worse than
none.

---

## Missing local tooling — verified absent

Checked directly. None of these is installed in a stock remote session:

| Tool | Needed by | Status |
|---|---|---|
| `ffmpeg` | video → frames for native vision | **absent** |
| `whisper` / `whisper.cpp` | local audio transcription, no API key | **absent** |
| `pandoc` | document conversion | **absent** |
| `tesseract` | OCR outside the built-in `pdf` skill | **absent** |
| `gh` | GitHub CLI | **absent** — use the `mcp__github__*` tools |

**Any capability depending on these must detect the absence and report it.** Silent
failure and pretending the tool ran are both worse than saying it is not here. This is
why `deep-module-architecture` degrades to markdown output when the GitHub MCP tools are
unavailable rather than shelling out to `gh`.

Installing them is the user's call on their own machine; see `integrations/media.md`.

## GitHub access

All GitHub work goes through the `mcp__github__*` MCP tools, loaded on demand via
`ToolSearch`. There is no `gh` CLI and no direct API access.

**The connected GitHub App has no Administration permission.**
`mcp__github__create_repository` fails with `403 Resource not accessible by integration`,
for personal accounts and organisations alike. Files, branches, pull requests, and issues
in already-authorised repositories work normally; **creating a new repository does not**.
A new repository has to be created by hand and then attached with `add_repo`.

Repository access is scoped per session. If `add_repo` reports the repository exists but
is not enabled for the workspace, an administrator grants access in the Claude GitHub
settings; a user reconnects their own authorisation under claude.ai Settings →
Connectors.

## The container is ephemeral

Provisioned clean at session start, reclaimed after inactivity. **Nothing survives
without `git commit` and `git push`.**

Writable disk is a fixed per-session allowance, so `df` misleads: `Avail` at 0 with low
`Used` means the allowance is spent, not that the disk is broken.

## Network

Outbound HTTPS goes through a preconfigured agent proxy, CA bundle at
`/root/.ccr/ca-bundle.crt`. Diagnose TLS or 403/405/407 failures with
`curl -sS "$HTTPS_PROXY/__agentproxy/status"`. **Never disable TLS verification and never
unset `HTTPS_PROXY`.**

## Browser

Chromium is preinstalled at `/opt/pw-browsers`, with `PLAYWRIGHT_BROWSERS_PATH` and
`PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1` already set. Do not run `playwright install`. This
is why `integrations/browser.md` documents the browser MCP servers without installing
one — a driveable browser is already here.

## Account-synced skills double-load

Several skills in this repository also exist as custom skills synced on the claude.ai
account, so both copies load in the same session. **The repository is the source of
truth**, and until the account copies are retired through the claude.ai UI, part of the
context saving from this restructuring is cancelled.

`scripts/validate.sh` warns when it detects the overlap. See `audit-2026-08.md` §4.1 for
the list.
