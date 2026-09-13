# Release process

This repository prepares releases but does not automatically publish to PyPI.

## Preflight

1. Confirm the intended version in `pyproject.toml`, `VERSION`, and
   `src/ha_controller/__init__.py`.
2. Move relevant entries from Unreleased into the version section.
3. Review `docs/releases/v0.1.0.md` or create notes for the new version.
4. Run:

```bash
ruff check .
ruff format --check .
mypy src
pytest
rm -rf build dist *.egg-info
python -m build
twine check dist/*
```

5. Install the wheel into a clean environment and run `ha-controller --help`.
6. Merge through a pull request and wait for green CI on `main`.

## GitHub release

Create an annotated tag from the reviewed commit:

```bash
git switch main
git pull --ff-only
git tag -a v0.1.0 -m "v0.1.0"
git push origin v0.1.0
```

Draft a GitHub release for that tag, paste the reviewed release notes, mark it as
a pre-release while the API is alpha, and optionally attach the wheel and source
distribution produced from the tagged commit.

## PyPI

Do not publish until the package name, project ownership, trusted publishing,
and maintainer recovery procedures are configured. If publication is later
enabled, prefer PyPI trusted publishing instead of a long-lived API token.
