# Architecture

The transport layer owns HTTP and Home Assistant formats. The model layer converts payloads into typed objects. The pure rules layer receives state and returns a proposed action without network access. A later execution layer can approve, suppress, rate-limit or apply it.

Recommended data flow:

1. Read state.
2. Parse EntityState.
3. Evaluate rules.
4. Write a structured decision trace.
5. Execute only in apply mode.
6. Read state again and verify the outcome.

Timeouts and authorization errors are failures, not false sensor values. Safety functions must remain in device-local controls and certified protective hardware.