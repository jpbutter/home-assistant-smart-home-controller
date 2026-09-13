# Architecture

## Design goal

The project makes the boundary between observation and execution explicit. Code
that reads remote state is separated from code that decides what could happen.

## Components

### REST client

`HomeAssistantClient` owns bearer authentication, HTTP transport, endpoint
paths, response-status checks, JSON-shape validation, and connection cleanup. It
implements only documented Home Assistant REST endpoints.

### Entity model

`EntityState` converts untyped JSON into a small local model. Required fields
and attribute shapes are checked at the boundary. The numeric-state property
returns `None` when Home Assistant exposes states such as `unknown` or
`unavailable`.

### Rule model

`ThresholdRule` is pure: it receives an `EntityState` and returns either
`None` or a `ProposedAction`. It does not know about tokens, HTTP, retries, or
Home Assistant clients.

### CLI

The CLI is intentionally read-only in v0.1.0. It checks the API and prints one
entity state. Service execution remains an explicit library call.

## Intended execution flow

1. Read and validate remote state.
2. Reject missing, malformed, or stale inputs.
3. Evaluate rules without side effects.
4. Record the proposal and reason.
5. Apply policy, cooldown, and idempotency checks.
6. Execute only in an explicit apply mode.
7. Read state again and verify the intended result.

Steps 4–7 are architectural guidance; v0.1.0 implements steps 1–3 and the
low-level service-call primitive.

## Error model

HTTP failures and unexpected response shapes raise `HomeAssistantError`.
Invalid local arguments raise `ValueError`. A network problem is never converted
to a false sensor reading.

## Dependency boundary

`httpx` is the sole runtime dependency. Tests replace its transport with
`MockTransport`, so no network or Home Assistant instance is needed.
