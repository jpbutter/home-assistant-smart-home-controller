import pytest

from ha_controller.cli import _settings


def test_settings_reads_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOME_ASSISTANT_URL", "http://homeassistant.test:8123")
    monkeypatch.setenv("HOME_ASSISTANT_TOKEN", "test-token")
    assert _settings() == ("http://homeassistant.test:8123", "test-token")


def test_settings_reports_all_missing_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("HOME_ASSISTANT_URL", raising=False)
    monkeypatch.delenv("HOME_ASSISTANT_TOKEN", raising=False)
    with pytest.raises(
        ValueError,
        match="missing required environment variables: HOME_ASSISTANT_URL, HOME_ASSISTANT_TOKEN",
    ):
        _settings()


def test_settings_reports_only_the_missing_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOME_ASSISTANT_URL", "http://homeassistant.test:8123")
    monkeypatch.delenv("HOME_ASSISTANT_TOKEN", raising=False)
    with pytest.raises(
        ValueError,
        match="missing required environment variables: HOME_ASSISTANT_TOKEN",
    ):
        _settings()
