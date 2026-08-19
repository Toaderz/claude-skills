# Browser

## What is already here

**Chromium is preinstalled** in a Claude Code remote session, at `/opt/pw-browsers`, with
`PLAYWRIGHT_BROWSERS_PATH` and `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1` already set.

**Do not run `playwright install`.** For scripted browser work — take a screenshot, fill a
form, scrape a rendered page — write a Playwright script and run it. No MCP server is
needed for that, and none is installed here.

## When an MCP server earns its cost

Only when Claude needs to *drive* the browser interactively across a task: click, read the
result, decide, click again. A script cannot do that; it has to know the steps in advance.

| Option | Maintainer | Cost per request | Notes |
|---|---|---:|---|
| Playwright MCP | Microsoft | **~13.7k tokens** | Broad tool surface, actively maintained |
| Chrome DevTools MCP | Google | **~19k tokens** | Adds performance and network inspection |

**Those numbers are the whole decision.** ~13.7k tokens per request is more than twenty
times this library's entire ambient footprint. Install one for a session that genuinely
needs interactive browsing, and remove it after.

```bash
claude mcp add playwright npx '@playwright/mcp@latest'   # then remove when done
```

## What to check before installing

Both are first-party servers from large vendors, which is the reason they are the two
listed. A browser MCP can navigate anywhere and read anything rendered, **including pages
where you are already authenticated**. Treat it as a credentialed capability, not a
utility.
