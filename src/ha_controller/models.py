from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class EntityState:
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
    def from_api(cls, payload: dict[str, Any]) -> "EntityState":
        changed = payload.get("last_changed")
        return cls(
            entity_id=str(payload["entity_id"]),
            state=str(payload["state"]),
            attributes=dict(payload.get("attributes", {})),
            last_changed=datetime.fromisoformat(changed.replace("Z", "+00:00")) if changed else None,
        )
