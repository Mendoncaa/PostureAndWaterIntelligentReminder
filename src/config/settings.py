import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "activity_threshold_minutes": 50,
    "idle_reset_minutes": 5,
    "repeat_interval_minutes": 10,
    "notification_title": "🥤 Alerta de Hidratação & Postura",
    "show_tray_icon": True,
    "enabled": True,
}

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config.json"

_VALIDATION_RULES = {
    "activity_threshold_minutes": (1, 480),   # 1 min to 8 hours
    "idle_reset_minutes": (1, 60),            # 1 min to 1 hour
    "repeat_interval_minutes": (1, 60),       # 1 min to 1 hour
}


def _validate_settings(config: dict) -> dict:
    """Validate and clamp config values to safe ranges."""
    for key, (min_val, max_val) in _VALIDATION_RULES.items():
        if key in config:
            value = config[key]
            if not isinstance(value, (int, float)) or value < min_val:
                logger.warning(f"Config '{key}' = {value} inválido. Usando mínimo: {min_val}")
                config[key] = min_val
            elif value > max_val:
                logger.warning(f"Config '{key}' = {value} demasiado alto. Usando máximo: {max_val}")
                config[key] = max_val

    # Validate boolean fields
    for key in ("enabled", "show_tray_icon"):
        if key in config and not isinstance(config[key], bool):
            logger.warning(f"Config '{key}' = {config[key]!r} não é booleano. Usando default.")
            config[key] = DEFAULT_CONFIG[key]

    # Validate string fields
    if "notification_title" in config and not isinstance(config["notification_title"], str):
        logger.warning("Config 'notification_title' inválido. Usando default.")
        config["notification_title"] = DEFAULT_CONFIG["notification_title"]

    return config


def load_settings() -> dict:
    config = DEFAULT_CONFIG.copy()

    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                user_config = json.load(f)
            for key in DEFAULT_CONFIG:
                if key in user_config:
                    config[key] = user_config[key]
        except (json.JSONDecodeError, OSError) as e:
            logger.error(f"Erro ao ler config.json: {e}. Usando defaults.")

    return _validate_settings(config)


def get_activity_threshold_seconds(settings: dict) -> int:
    return settings["activity_threshold_minutes"] * 60


def get_idle_reset_seconds(settings: dict) -> int:
    return settings["idle_reset_minutes"] * 60


def get_repeat_interval_seconds(settings: dict) -> int:
    return settings["repeat_interval_minutes"] * 60
