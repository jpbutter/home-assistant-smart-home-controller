from collections.abc import Mapping
from dataclasses import dataclass
from math import isfinite
from typing import Any

from .models import EntityState


@dataclass(frozen=True)
class ProposedAction:
    """An action proposal that has not been sent to Home Assistant."""

    domain: str
    service: str
    data: Mapping[str, Any]
    reason: str


@dataclass(frozen=True)
class ThresholdRule:
    """Propose a service call when a numeric entity state exceeds a threshold."""

    source_entity: str
    above: float
    target_entity: str
    service: str

    def __post_init__(self) -> None:
        if not self.source_entity or not self.target_entity:
            raise ValueError("source_entity and target_entity must not be empty")
        if not isfinite(self.above):
            raise ValueError("above must be finite")
        if self.service.count(".") != 1 or any(not part for part in self.service.split(".")):
            raise ValueError("service must use the domain.service format")

    def evaluate(self, state: EntityState) -> ProposedAction | None:
        if state.entity_id != self.source_entity:
            return None
        value = state.numeric_state
        if value is None or value <= self.above:
            return None

        domain, service_name = self.service.split(".", maxsplit=1)
        return ProposedAction(
            domain=domain,
            service=service_name,
            data={"entity_id": self.target_entity},
            reason=f"{self.source_entity} is {value}, above {self.above}",
        )
