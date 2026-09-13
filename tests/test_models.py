import pytest

from ha_controller.models import EntityState


def test_unknown_state_is_not_numeric() -> None:
    state = EntityState("sensor.demo", "unavailable", {}, None)
    assert state.numeric_state is None


def test_model_rejects_missing_required_fields() -> None:
    with pytest.raises(ValueError, match="entity_id and state"):
        EntityState.from_api({"attributes": {}})


def test_model_rejects_non_object_attributes() -> None:
    with pytest.raises(ValueError, match="attributes"):
        EntityState.from_api({"entity_id": "sensor.demo", "state": "1", "attributes": []})
