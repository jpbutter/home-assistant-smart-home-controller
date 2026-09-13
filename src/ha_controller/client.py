from collections.abc import Mapping
from typing import Any, Self, cast

import httpx

from .models import EntityState


class HomeAssistantError(RuntimeError):
    """Raised for transport-successful but unusable Home Assistant responses."""


class HomeAssistantClient:
    """Minimal asynchronous client for documented Home Assistant REST endpoints."""

    def __init__(
        self,
        base_url: str,
        token: str,
        *,
        timeout: float = 10.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        if not base_url.strip():
            raise ValueError("base_url must not be empty")
        if not token.strip():
            raise ValueError("token must not be empty")

        self._client = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            timeout=timeout,
            transport=transport,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        await self._client.aclose()

    async def check_api(self) -> str:
        """Return the message from Home Assistant's API root endpoint."""
        response = await self._client.get("/api/")
        self._raise_for_status(response, "API check")
        payload = self._object_payload(response, "API check")
        message = payload.get("message")
        if not isinstance(message, str):
            raise HomeAssistantError("API check returned no string message")
        return message

    async def get_state(self, entity_id: str) -> EntityState:
        """Read and validate one entity state."""
        if not entity_id.strip():
            raise ValueError("entity_id must not be empty")
        response = await self._client.get(f"/api/states/{entity_id}")
        self._raise_for_status(response, "State request")
        return EntityState.from_api(self._object_payload(response, "State request"))

    async def get_states(self) -> list[EntityState]:
        """Read all currently known entity states."""
        response = await self._client.get("/api/states")
        self._raise_for_status(response, "States request")
        payload: object = response.json()
        if not isinstance(payload, list) or not all(isinstance(item, Mapping) for item in payload):
            raise HomeAssistantError("States request returned an unexpected JSON shape")
        items = cast(list[Mapping[str, Any]], payload)
        return [EntityState.from_api(item) for item in items]

    async def call_service(
        self,
        domain: str,
        service: str,
        data: Mapping[str, Any],
    ) -> list[dict[str, Any]]:
        """Call one Home Assistant service and return changed-state payloads."""
        if not domain.strip() or not service.strip():
            raise ValueError("domain and service must not be empty")
        response = await self._client.post(
            f"/api/services/{domain}/{service}",
            json=dict(data),
        )
        self._raise_for_status(response, "Service call")
        payload: object = response.json()
        if not isinstance(payload, list) or not all(isinstance(item, Mapping) for item in payload):
            raise HomeAssistantError("Service call returned an unexpected JSON shape")
        items = cast(list[Mapping[str, Any]], payload)
        return [dict(item) for item in items]

    @staticmethod
    def _raise_for_status(response: httpx.Response, operation: str) -> None:
        if not response.is_success:
            raise HomeAssistantError(f"{operation} failed: HTTP {response.status_code}")

    @staticmethod
    def _object_payload(response: httpx.Response, operation: str) -> Mapping[str, Any]:
        payload: object = response.json()
        if not isinstance(payload, Mapping):
            raise HomeAssistantError(f"{operation} returned an unexpected JSON shape")
        return cast(Mapping[str, Any], payload)
