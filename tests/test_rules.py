import pytest

from ha_controller.models import EntityState
from ha_controller.rules import ThresholdRule


def test_rule_proposes_action_above_threshold() -> None:
    state = EntityState("sensor.demo_temperature", "29.2", {}, None)
    rule = ThresholdRule("sensor.demo_temperature", 28.0, "fan.demo", "fan.turn_on")
    action = rule.evaluate(state)
    assert action is not None
    assert action.domain == "fan"
    assert action.service == "turn_on"
    assert action.data == {"entity_id": "fan.demo"}
    assert "above 28.0" in action.reason


@pytest.mark.parametrize("value", ["28.0", "unavailable"])
def test_rule_ignores_non_triggering_values(value: str) -> None:
    state = EntityState("sensor.demo", value, {}, None)
    rule = ThresholdRule("sensor.demo", 28.0, "fan.demo", "fan.turn_on")
    assert rule.evaluate(state) is None


def test_rule_ignores_unrelated_state() -> None:
    state = EntityState("sensor.other", "40", {}, None)
    rule = ThresholdRule("sensor.demo", 28.0, "fan.demo", "fan.turn_on")
    assert rule.evaluate(state) is None


@pytest.mark.parametrize("service", ["turn_on", ".turn_on", "fan.", "fan.turn.on"])
def test_rule_rejects_invalid_service(service: str) -> None:
    with pytest.raises(ValueError, match=r"domain\.service"):
        ThresholdRule("sensor.demo", 28.0, "fan.demo", service)
