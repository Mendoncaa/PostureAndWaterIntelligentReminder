import json
import os
from pathlib import Path

DEFAULT_CONFIG = {
    "activity_threshold_minutes": 50,
    "idle_reset_minutes": 5,
    "notification_title": "🥤 Alerta de Hidratação & Postura",
    "enabled": True,
}

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config.json"


def load_settings() -> dict:
    config = DEFAULT_CONFIG.copy()

    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            user_config = json.load(f)
        for key in DEFAULT_CONFIG:
            if key in user_config:
                config[key] = user_config[key]

    return config


def get_activity_threshold_seconds(settings: dict) -> int:
    return settings["activity_threshold_minutes"] * 60


def get_idle_reset_seconds(settings: dict) -> int:
    return settings["idle_reset_minutes"] * 60
