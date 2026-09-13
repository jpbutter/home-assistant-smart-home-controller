from typing import Any

import httpx

from .models import EntityState


class HomeAssistantError(RuntimeError):
    pass


class HomeAssistantClient:
    def __init__(
        self,
        base_url: str,
        token: str,
        *,
        timeout: float = 10.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            timeout=timeout,
            transport=transport,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        )

    async def __aenter__(self) -> "HomeAssistantClient":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self._client.aclose()

    async def get_state(self, entity_id: str) -> EntityState:
        response = await self._client.get(f"/api/states/{entity_id}")
        if not response.is_success:
            raise HomeAssistantError(f"State request failed: HTTP {response.status_code}")
        return EntityState.from_api(response.json())

    async def call_service(
        self, domain: str, service: str, data: dict[str, Any]
    ) -> list[dict[str, Any]]:
        response = await self._client.post(f"/api/services/{domain}/{service}", json=data)
        if not response.is_success:
            raise HomeAssistantError(f"Service call failed: HTTP {response.status_code}")
        return list(response.json())
