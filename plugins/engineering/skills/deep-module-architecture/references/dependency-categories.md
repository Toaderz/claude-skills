# Dependency categories, testing strategy, and the RFC template

Read this at step 2 (classifying a candidate) and step 6 (writing the RFC).

---

## The four dependency categories

Classify every dependency of a deepening candidate. The category decides whether the
module can be deepened at all, and how its tests will run.

### 1. In-process

Pure computation, in-memory state, no I/O. **Always deepenable** — merge the modules and
test directly.

### 2. Local-substitutable

Has a local test stand-in (PGLite for Postgres, an in-memory filesystem). Deepenable if
the substitute exists. The deepened module is tested with the stand-in running in the
suite.

### 3. Remote but owned — ports and adapters

Your own services across a network boundary: microservices, internal APIs. Define a port
at the module boundary. The deep module owns the logic; the transport is injected. Tests
use an in-memory adapter, production uses the real HTTP/gRPC/queue one.

> Recommendation shape: "Define a shared port, implement an HTTP adapter for production
> and an in-memory adapter for testing, so the logic is tested as one deep module even
> though it deploys across a network boundary."

### 4. True external — mock

Third-party services you do not control (Stripe, Twilio). Mock at the boundary. The
deepened module takes the dependency as an injected port; tests supply a mock.

---

## Testing strategy

The core principle: **replace, do not layer.**

- Old unit tests on shallow modules become waste once boundary tests exist — delete them.
- Write new tests at the deepened module's interface boundary.
- Assert on observable outcomes through the public interface, never on internal state.
- Tests should survive internal refactors: they describe behaviour, not implementation.

A deepening that adds boundary tests **on top of** the old unit tests has not deepened
anything. It has added a layer.

---

## RFC template

```markdown
## Problem
- Which modules are shallow and tightly coupled
- What integration risk lives in the seams between them
- Why this makes the codebase harder to navigate and maintain

## Proposed interface
- Interface signature (types, methods, params)
- Usage example showing how callers use it
- What complexity it hides internally

## Dependency strategy
Which category applies, and how dependencies are handled:
- In-process: merged directly
- Local-substitutable: tested with [specific stand-in]
- Ports and adapters: port definition, production adapter, test adapter
- Mock: mock boundary for external services

## Testing strategy
- New boundary tests to write: the behaviours to verify at the interface
- Old tests to delete: the shallow-module tests that become redundant
- Test environment needs: local stand-ins or adapters required

## Implementation recommendations
Durable guidance, NOT coupled to current file paths:
- What the module should own (responsibilities)
- What it should hide (implementation details)
- What it should expose (the interface contract)
- How callers migrate to the new interface
```

**Why the last section avoids file paths:** an RFC that names `src/parsers/v2/table.py`
is stale the first time someone moves a file. One that names responsibilities survives.
