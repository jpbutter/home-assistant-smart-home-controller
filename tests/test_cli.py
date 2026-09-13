import pytest

from ha_controller.cli import _settings


def test_settings_reads_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOME_ASSISTANT_URL", "http://homeassistant.test:8123")
    monkeypatch.setenv("HOME_ASSISTANT_TOKEN", "test-token")
    assert _settings() == ("http://homeassistant.test:8123", "test-token")


def test_settings_requires_both_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("HOME_ASSISTANT_URL", raising=False)
    monkeypatch.delenv("HOME_ASSISTANT_TOKEN", raising=False)
    with pytest.raises(ValueError, match="are required"):
        _settings()
