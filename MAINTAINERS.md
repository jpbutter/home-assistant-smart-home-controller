# Maintainers

## Current maintainer

- [@jpbutter](https://github.com/jpbutter) — project direction, reviews,
  releases, and security triage.

## Responsibilities

Maintainers:

- keep `main` buildable and review CI failures;
- triage issues for scope, reproducibility, and safety implications;
- review dependency updates and package metadata;
- ensure behavior changes include tests and documentation;
- coordinate vulnerability handling privately;
- create releases from reviewed commits using the release runbook.

## Decision model

Routine changes are accepted through reviewed pull requests. For changes to the
public API, security model, dependency strategy, or project scope, the maintainer
records the rationale in the pull request or a linked issue.

## Release authority

Only maintainers create tags and GitHub releases. A release requires green CI,
matching version declarations, validated distributions, updated release notes,
and a clean working tree. See [docs/releasing.md](docs/releasing.md).

## Adding maintainers

New maintainers should have a sustained history of careful contributions and
sound handling of security- or safety-sensitive changes. Additions are recorded
in this file and CODEOWNERS.
