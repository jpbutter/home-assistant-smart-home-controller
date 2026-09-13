# Home Assistant Smart Home Controller

An opinionated Python starter kit for small, testable control services around Home Assistant. It wraps the official REST API, models entity state explicitly and keeps automation decisions separate from network calls.

## Status

Version **0.1.0** is a developer preview. It reads entity states, calls services and evaluates simple threshold rules. The repository contains synthetic entity IDs only; no URL, access token or household data is committed.

## Motivation

Large smart-home installations become difficult to maintain when every decision is embedded inside one automation. This project explores a thin orchestration layer that keeps Home Assistant as the source of truth while making decisions testable without a running home.

Potential experiments include energy-aware charging, heating guardrails, ventilation prompts and room dashboards. Safety-critical functions must remain in certified local hardware.

## Quick start

~~~bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
export HOME_ASSISTANT_URL=http://homeassistant.local:8123
export HOME_ASSISTANT_TOKEN=replace-locally
ha-controller state sensor.demo_temperature
~~~

## Included

- Async REST client based on httpx
- Typed entity-state model
- Pure, dry-run-friendly rule engine
- Synthetic room and rule configuration
- Unit tests, CI and operational notes
- No embedded credentials

Requests use Home Assistant REST endpoints below **/api/** with a bearer token. The rule engine returns proposed actions; an execution layer decides whether to log, approve, rate-limit or apply them.