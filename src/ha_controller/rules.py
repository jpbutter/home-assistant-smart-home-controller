from dataclasses import dataclass
from typing import Any

from .models import EntityState


@dataclass(frozen=True)
class ProposedAction:
    domain: str
    service: str
    data: dict[str, Any]
    reason: str


@dataclass(frozen=True)
class ThresholdRule:
    source_entity: str
    above: float
    target_entity: str
    service: str

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
