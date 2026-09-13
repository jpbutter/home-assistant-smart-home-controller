from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self


@dataclass(frozen=True)
class EntityState:
    """Validated subset of a Home Assistant entity-state response."""

    entity_id: str
    state: str
    attributes: dict[str, Any]
    last_changed: datetime | None

    @property
    def numeric_state(self) -> float | None:
        try:
            return float(self.state)
        except (TypeError, ValueError):
            return None

    @classmethod
    def from_api(cls, payload: Mapping[str, Any]) -> Self:
        entity_id = payload.get("entity_id")
        state = payload.get("state")
        attributes = payload.get("attributes", {})
        changed = payload.get("last_changed")

        if not isinstance(entity_id, str) or not isinstance(state, str):
            raise ValueError("entity_id and state must be strings")
        if not isinstance(attributes, Mapping):
            raise ValueError("attributes must be an object")
        if changed is not None and not isinstance(changed, str):
            raise ValueError("last_changed must be a string or null")

        return cls(
            entity_id=entity_id,
            state=state,
            attributes=dict(attributes),
            last_changed=datetime.fromisoformat(changed) if changed else None,
        )
