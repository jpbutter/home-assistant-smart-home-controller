# Contributing

Thanks for considering a contribution. Small, reviewable pull requests are the
easiest to evaluate.

## Development setup

```bash
git clone https://github.com/jpbutter/home-assistant-smart-home-controller.git
cd home-assistant-smart-home-controller
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Run the same checks as CI:

```bash
ruff check .
ruff format --check .
mypy src
pytest
python -m build
twine check dist/*
```

## Pull requests

1. Open or reference an issue for behavior changes.
2. Keep the change focused and add tests.
3. Update public documentation and the Unreleased changelog section when needed.
4. Explain whether the change only reads data, proposes an action, or can call a
   Home Assistant service.
5. Confirm that examples and fixtures use synthetic identifiers and data.

Use clear commit messages; Conventional Commits are encouraged but not required.
A maintainer may request changes before merge.

## Scope and data hygiene

Do not commit tokens, exported Home Assistant databases, addresses, presence
history, camera images, real entity inventories, or other household telemetry.
New dependencies need a concrete purpose and must be reflected in package
metadata.

## Reporting security problems

Do not open a public issue for a vulnerability. Follow [SECURITY.md](SECURITY.md).
