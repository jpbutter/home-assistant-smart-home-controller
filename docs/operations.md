# Operations

Use three modes: **observe** reads data, **propose** logs intended actions and **apply** calls services. Every new rule should spend time in observe or propose mode.

Track request latency, stale-state age, API errors, proposals, executed actions, suppressed duplicates and verification failures. Use bounded retries only for operations that are safe to repeat.

Store tokens outside the repository. Do not log headers, presence histories or sensitive attributes. Home Assistant and essential local automations should continue operating if this service is unavailable.