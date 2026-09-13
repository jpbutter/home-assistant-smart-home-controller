from collections.abc import Callable

import httpx
import pytest

from ha_controller.client import HomeAssistantClient, HomeAssistantError


def transport(handler: Callable[[httpx.Request], httpx.Response]) -> httpx.MockTransport:
    return httpx.MockTransport(handler)


@pytest.mark.asyncio
async def test_check_api_returns_message_and_sends_bearer_token() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/"
        assert request.headers["Authorization"] == "Bearer test-token"
        return httpx.Response(200, json={"message": "API running."})

    async with HomeAssistantClient(
        "http://homeassistant.test:8123", "test-token", transport=transport(handler)
    ) as client:
        assert await client.check_api() == "API running."


@pytest.mark.asyncio
async def test_get_state_parses_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/states/sensor.demo_temperature"
        return httpx.Response(
            200,
            json={
                "entity_id": "sensor.demo_temperature",
                "state": "22.4",
                "attributes": {"unit_of_measurement": "°C"},
                "last_changed": "2026-09-13T07:30:00Z",
            },
        )

    async with HomeAssistantClient(
        "http://homeassistant.test:8123", "test-token", transport=transport(handler)
    ) as client:
        state = await client.get_state("sensor.demo_temperature")

    assert state.numeric_state == 22.4
    assert state.attributes["unit_of_measurement"] == "°C"


@pytest.mark.asyncio
async def test_get_states_parses_list() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json=[
                {
                    "entity_id": "sensor.one",
                    "state": "1",
                    "attributes": {},
                    "last_changed": None,
                }
            ],
        )

    async with HomeAssistantClient(
        "http://homeassistant.test:8123", "test-token", transport=transport(handler)
    ) as client:
        states = await client.get_states()

    assert [state.entity_id for state in states] == ["sensor.one"]


@pytest.mark.asyncio
async def test_call_service_returns_changed_states() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/services/light/turn_on"
        assert request.method == "POST"
        return httpx.Response(200, json=[{"entity_id": "light.demo", "state": "on"}])

    async with HomeAssistantClient(
        "http://homeassistant.test:8123", "test-token", transport=transport(handler)
    ) as client:
        changed = await client.call_service("light", "turn_on", {"entity_id": "light.demo"})

    assert changed[0]["state"] == "on"


@pytest.mark.asyncio
async def test_http_error_does_not_become_entity_state() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"message": "Unauthorized"})

    async with HomeAssistantClient(
        "http://homeassistant.test:8123", "test-token", transport=transport(handler)
    ) as client:
        with pytest.raises(HomeAssistantError, match="HTTP 401"):
            await client.get_state("sensor.demo")


@pytest.mark.asyncio
async def test_unexpected_json_shape_is_rejected() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=["not", "an", "object"])

    async with HomeAssistantClient(
        "http://homeassistant.test:8123", "test-token", transport=transport(handler)
    ) as client:
        with pytest.raises(HomeAssistantError, match="unexpected JSON shape"):
            await client.get_state("sensor.demo")


def test_client_rejects_empty_connection_values() -> None:
    with pytest.raises(ValueError, match="base_url"):
        HomeAssistantClient("", "token")
    with pytest.raises(ValueError, match="token"):
        HomeAssistantClient("http://homeassistant.test", "")
