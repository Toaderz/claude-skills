# Integrations

External capabilities this library **documents but does not install**.

Every file here answers the same three questions: what the official option is, what it
costs, and what you have to do yourself. Nothing in this directory installs anything or
asks for a credential.

| File | Covers |
|---|---|
| [`browser.md`](browser.md) | driving a real browser |
| [`email.md`](email.md) | reading and sending mail |
| [`media.md`](media.md) | video and audio |
| [`github.md`](github.md) | repositories, pull requests, issues |
| [`security-tools.md`](security-tools.md) | static analysis beyond `/security-review` |

## Why documented and not installed

An MCP server is not free. Its tool definitions are loaded into context, and a heavyweight
one costs more per request than every skill in this library costs in a whole session.
Installing one "just in case" is a permanent tax for an occasional need.

Worse, an MCP server is code that runs with your credentials. **Before installing
anything external, inspect it**: who maintains it, what permissions it asks for, what its
install script does, what it reaches on the network, what files it touches, and whether
the code is obfuscated. Prefer an official Anthropic connector, then an official
first-party server, then a local CLI. A community MCP that wants OAuth access to your
email is the last resort, not the first.
