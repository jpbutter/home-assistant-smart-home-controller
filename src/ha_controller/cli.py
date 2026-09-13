import argparse
import asyncio
import json
import os

from .client import HomeAssistantClient


async def show_state(entity_id: str) -> None:
    async with HomeAssistantClient(
        os.environ["HOME_ASSISTANT_URL"],
        os.environ["HOME_ASSISTANT_TOKEN"],
    ) as client:
        state = await client.get_state(entity_id)
        print(json.dumps({"entity_id": state.entity_id, "state": state.state}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    state_parser = subparsers.add_parser("state")
    state_parser.add_argument("entity_id")
    args = parser.parse_args()
    if args.command == "state":
        asyncio.run(show_state(args.entity_id))


if __name__ == "__main__":
    main()
