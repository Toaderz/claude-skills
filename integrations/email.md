# Email

## Use the official connector

Anthropic ships a Gmail connector for claude.ai. **Authorise it there** — Settings →
Connectors — and it is available without anything installed in this repository.

That authorisation is yours to give and cannot be done from a session; it requires your
login.

## Do not install a community email MCP

There are several. They ask for OAuth access to your mailbox, or for an app password, and
they are maintained by individuals.

**The trade is bad on its face:** full read and send access to your email, granted to code
you did not audit, to save a step that an official connector already covers. An email
account is usually the reset path for every other account you own.

If the official connector does not cover your case, the honest fallback is to say so
rather than reach for an unvetted server.

## What this library does about email

Nothing, deliberately. There is no email skill. A skill cannot send mail — it would need
a tool underneath it, and that tool is the connector. Writing an `email-drafting` skill
would add ambient cost to produce text the model already writes well.

The eval case `10-email` asserts exactly this: on an email request, **no repository skill
should fire**. Either the connector handles it, or the absence is reported plainly.
