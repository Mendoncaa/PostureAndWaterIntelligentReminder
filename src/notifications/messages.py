import json
import random
from pathlib import Path


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
        with open(self._messages_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._messages = data["messages"]
        self._remaining = self._messages.copy()
        random.shuffle(self._remaining)

    def get_message(self, minutes: int = 50) -> str:
        """Get next message, cycling through all before repeating."""
        if not self._remaining:
            self._remaining = self._messages.copy()
            random.shuffle(self._remaining)

        message = self._remaining.pop()
        return message.format(minutes=minutes)

    @property
    def total_messages(self) -> int:
        return len(self._messages)
