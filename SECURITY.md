# Security Policy

## Supported versions

Before the first stable release, only the latest tagged minor version and the
current `main` branch receive security fixes.

## Reporting a vulnerability

Use GitHub's private **Report a vulnerability** flow under the repository's
Security tab. Do not include credentials, private URLs, entity inventories, or
household telemetry in a public issue.

Include the affected version, impact, reproduction steps using synthetic data,
and any suggested mitigation. No response-time guarantee is made; maintainers
will acknowledge and assess reports as availability permits.

## Credential exposure

If a Home Assistant token is exposed, revoke it in Home Assistant immediately
and create a replacement. Removing a token from the latest commit or rewriting
Git history does not invalidate copies already retrieved.

## Safety boundary

This package is general-purpose integration software, not safety-certified
control equipment. It must not be the sole protection for locks, alarms,
overcurrent, overheating, fire, water damage, or other hazards. Keep essential
fallback automations local and preserve device-level safeguards.
