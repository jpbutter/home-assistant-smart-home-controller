# Roadmap

This roadmap communicates direction, not deadlines or commitments.

## v0.2 — Safer execution

- Introduce explicit observe, propose, and apply modes.
- Add idempotency windows, cooldowns, and per-service rate limits.
- Record structured decision traces.
- Verify entity state after an applied action.

## v0.3 — Live state

- Add an optional Home Assistant WebSocket adapter.
- Reconnect with bounded exponential backoff.
- Detect and reject stale entity state.
- Add a bounded in-memory state cache.

## v0.4 — Configuration and energy examples

- Define and validate a versioned configuration schema.
- Load rules only after schema validation.
- Add PV-surplus and EV-charging hysteresis examples.
- Keep device- and vendor-specific behavior behind adapters.

## Long-term quality

- Document compatibility against supported Home Assistant releases.
- Add contract tests against a disposable Home Assistant test instance.
- Define deprecation and stable-API policies before v1.0.

## Non-goals

- Replacing Home Assistant.
- Providing a hosted cloud control plane.
- Acting as the only controller for alarms, access control, electrical
  protection, heating limits, or other safety-critical functions.
