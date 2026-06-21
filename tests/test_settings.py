import json
import tempfile
from pathlib import Path
from unittest.mock import patch
import pytest

from src.config.settings import load_settings, _validate_settings, DEFAULT_CONFIG


class TestSettings:
    def test_default_config_values(self):
        settings = DEFAULT_CONFIG.copy()
        assert settings["activity_threshold_minutes"] == 50
        assert settings["idle_reset_minutes"] == 5
        assert settings["enabled"] is True

    def test_validate_clamps_too_low(self):
        config = {"activity_threshold_minutes": 0, "idle_reset_minutes": -1}
        result = _validate_settings(config)
        assert result["activity_threshold_minutes"] == 1
        assert result["idle_reset_minutes"] == 1

    def test_validate_clamps_too_high(self):
        config = {"activity_threshold_minutes": 9999, "idle_reset_minutes": 999}
        result = _validate_settings(config)
        assert result["activity_threshold_minutes"] == 480
        assert result["idle_reset_minutes"] == 60

    def test_validate_accepts_valid_values(self):
        config = {"activity_threshold_minutes": 25, "idle_reset_minutes": 10}
        result = _validate_settings(config)
        assert result["activity_threshold_minutes"] == 25
        assert result["idle_reset_minutes"] == 10

    def test_load_settings_with_valid_file(self, tmp_path):
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "activity_threshold_minutes": 30,
            "idle_reset_minutes": 3,
        }), encoding="utf-8")

        with patch("src.config.settings.CONFIG_PATH", config_file):
            settings = load_settings()
            assert settings["activity_threshold_minutes"] == 30
            assert settings["idle_reset_minutes"] == 3

    def test_load_settings_missing_file_uses_defaults(self, tmp_path):
        fake_path = tmp_path / "nonexistent.json"
        with patch("src.config.settings.CONFIG_PATH", fake_path):
            settings = load_settings()
            assert settings == DEFAULT_CONFIG

    def test_load_settings_malformed_json_uses_defaults(self, tmp_path):
        config_file = tmp_path / "config.json"
        config_file.write_text("{ invalid json !!!", encoding="utf-8")

        with patch("src.config.settings.CONFIG_PATH", config_file):
            settings = load_settings()
            assert settings["activity_threshold_minutes"] == DEFAULT_CONFIG["activity_threshold_minutes"]
            assert settings == DEFAULT_CONFIG

    def test_validate_boolean_fields(self):
        config = {
            "enabled": "yes",  # Not a bool
            "show_tray_icon": 1,  # Not a bool
            "activity_threshold_minutes": 50,
            "idle_reset_minutes": 5,
        }
        result = _validate_settings(config)
        assert result["enabled"] == DEFAULT_CONFIG["enabled"]
        assert result["show_tray_icon"] == DEFAULT_CONFIG["show_tray_icon"]

    def test_validate_string_field(self):
        config = {
            "notification_title": 123,  # Not a string
            "activity_threshold_minutes": 50,
            "idle_reset_minutes": 5,
        }
        result = _validate_settings(config)
        assert result["notification_title"] == DEFAULT_CONFIG["notification_title"]

    def test_validate_accepts_valid_booleans(self):
        config = {"enabled": False, "show_tray_icon": True}
        result = _validate_settings(config)
        assert result["enabled"] is False
        assert result["show_tray_icon"] is True
