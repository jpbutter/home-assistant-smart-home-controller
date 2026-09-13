# Changelog

All notable changes are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- No changes recorded yet.

## [0.1.0] - 2026-09-13

### Added

- Asynchronous client for the documented Home Assistant REST API root, state,
  state-list, and service endpoints.
- Validated, typed entity-state model.
- Pure threshold-rule evaluation that produces an action proposal without
  performing a service call.
- CLI commands for connectivity checks and reading an entity.
- Synthetic configuration examples.
- Python 3.11–3.14 CI matrix, Ruff checks, strict mypy checks, pytest suite, and
  distribution build validation.
- Contributor, security, support, maintainer, and release documentation.
- Issue forms, pull-request template, CODEOWNERS, Dependabot configuration, and
  generated-release-notes configuration.

### Security

- Tokens are accepted only at runtime and are excluded from version control.
- Network errors and unexpected response shapes fail explicitly.

[Unreleased]: https://github.com/jpbutter/home-assistant-smart-home-controller/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/jpbutter/home-assistant-smart-home-controller/releases/tag/v0.1.0
