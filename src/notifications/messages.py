import json
import logging
import random
from pathlib import Path

logger = logging.getLogger(__name__)

_FALLBACK_MESSAGES = [
    "Estás a trabalhar há {minutes} minutos. Vai beber água e estica as costas!",
    "Pausa! O teu corpo agradece. Hidrata-te.",
]


class MessageLoader:
    """Loads and serves messages without immediate repetition."""

    def __init__(self, messages_path: Path = None):
        if messages_path is None:
            messages_path = Path(__file__).resolve().parent.parent.parent / "data" / "messages.json"

        self._messages_path = messages_path
        self._messages = []
        self._remaining = []
        self._load_messages()

    def _load_messages(self):
        try:
            with open(self._messages_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            messages = data.get("messages", [])
            if not isinstance(messages, list) or not messages:
                raise ValueError("'messages' vazio ou inválido")
            self._messages = messages
        except (OSError, json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Erro ao carregar mensagens ({e}). Usando fallback.")
            self._messages = _FALLBACK_MESSAGES.copy()

        self._remaining = self._messages.copy()
        random.shuffle(self._remaining)

    def get_message(self, minutes: int = 50) -> str:
        """Get next message, cycling through all before repeating."""
        if not self._remaining:
            self._remaining = self._messages.copy()
            random.shuffle(self._remaining)

        message = self._remaining.pop()
        try:
            return message.replace("{minutes}", str(minutes))
        except (KeyError, ValueError):
            return message

    @property
    def total_messages(self) -> int:
        return len(self._messages)
