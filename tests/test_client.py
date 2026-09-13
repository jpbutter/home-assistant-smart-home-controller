import httpx
import pytest

from ha_controller.client import HomeAssistantClient


@pytest.mark.asyncio
async def test_get_state_parses_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer test-token"
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
        "http://homeassistant.test:8123",
        "test-token",
        transport=httpx.MockTransport(handler),
    ) as client:
        state = await client.get_state("sensor.demo_temperature")
    assert state.numeric_state == 22.4
