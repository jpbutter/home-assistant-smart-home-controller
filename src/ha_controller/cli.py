import argparse
import asyncio
import json
import os

from .client import HomeAssistantClient, HomeAssistantError


def _settings() -> tuple[str, str]:
    url = os.getenv("HOME_ASSISTANT_URL")
    token = os.getenv("HOME_ASSISTANT_TOKEN")
    if not url or not token:
        raise ValueError("HOME_ASSISTANT_URL and HOME_ASSISTANT_TOKEN are required")
    return url, token


async def _check() -> None:
    url, token = _settings()
    async with HomeAssistantClient(url, token) as client:
        print(await client.check_api())


async def _show_state(entity_id: str) -> None:
    url, token = _settings()
    async with HomeAssistantClient(url, token) as client:
        state = await client.get_state(entity_id)
        print(
            json.dumps(
                {
                    "entity_id": state.entity_id,
                    "state": state.state,
                    "attributes": state.attributes,
                    "last_changed": state.last_changed.isoformat() if state.last_changed else None,
                },
                indent=2,
                ensure_ascii=False,
            )
        )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ha-controller",
        description="Inspect a Home Assistant API connection and entity states.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("check", help="Verify API reachability and authentication")
    state_parser = subparsers.add_parser("state", help="Read one entity state")
    state_parser.add_argument("entity_id")
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.command == "check":
            asyncio.run(_check())
        elif args.command == "state":
            asyncio.run(_show_state(args.entity_id))
    except (HomeAssistantError, ValueError) as exc:
        print(f"error: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
