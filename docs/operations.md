# Operations

## Recommended modes

- **Observe:** read state and emit metrics only.
- **Propose:** evaluate and record intended actions.
- **Apply:** execute reviewed actions with cooldowns and verification.

Version 0.1.0 supplies read operations, proposal logic, and an explicit
service-call primitive. It does not implement a production executor.

## Useful telemetry

Track API latency, HTTP failures, invalid response shapes, state age, proposed
actions, executed actions, suppressed duplicates, and verification failures.
Process health alone does not prove that devices are reachable.

## Secrets

Inject the token at runtime. Do not print request headers or environment
variables. Use a dedicated token and rotate it after any suspected exposure.
Repository examples contain placeholders only.

## Failure and recovery

Use bounded retries only for operations known to be safe to repeat. Home
Assistant and essential local automations should continue to operate when an
external controller is unavailable. Do not replay an unbounded queue of stale
actions after recovery.

## Deployment checklist

- Pin a reviewed package version or commit.
- Use an isolated environment and a non-root process.
- Restrict network access to the Home Assistant instance where practical.
- Configure timeouts and external process supervision.
- Start with observation or proposal behavior.
- Test loss of Home Assistant, invalid tokens, and stale states.
