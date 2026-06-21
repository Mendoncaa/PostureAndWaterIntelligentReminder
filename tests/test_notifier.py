import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from src.notifications.messages import MessageLoader
from src.notifications.notifier import Notifier


class TestMessageLoader:
    def _create_temp_messages(self, messages):
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8")
        json.dump({"messages": messages}, tmp)
        tmp.close()
        return Path(tmp.name)

    def test_loads_messages_from_file(self):
        path = self._create_temp_messages(["msg1", "msg2", "msg3"])
        loader = MessageLoader(messages_path=path)
        assert loader.total_messages == 3

    def test_get_message_returns_string(self):
        path = self._create_temp_messages(["Hello {minutes} min"])
        loader = MessageLoader(messages_path=path)
        msg = loader.get_message(minutes=50)
        assert msg == "Hello 50 min"

    def test_no_immediate_repetition(self):
        messages = [f"msg{i}" for i in range(5)]
        path = self._create_temp_messages(messages)
        loader = MessageLoader(messages_path=path)

        seen = []
        for _ in range(5):
            msg = loader.get_message()
            assert msg not in seen
            seen.append(msg)

    def test_cycles_after_exhaustion(self):
        path = self._create_temp_messages(["only_one"])
        loader = MessageLoader(messages_path=path)

        msg1 = loader.get_message()
        msg2 = loader.get_message()
        assert msg1 == "only_one"
        assert msg2 == "only_one"

    def test_format_minutes_placeholder(self):
        path = self._create_temp_messages(["Coding for {minutes} minutes"])
        loader = MessageLoader(messages_path=path)
        msg = loader.get_message(minutes=30)
        assert "30" in msg

    def test_loads_default_messages_file(self):
        loader = MessageLoader()
        assert loader.total_messages >= 10

    def test_missing_file_uses_fallback(self, tmp_path):
        fake_path = tmp_path / "nonexistent.json"
        loader = MessageLoader(messages_path=fake_path)
        assert loader.total_messages >= 1
        msg = loader.get_message(minutes=25)
        assert "25" in msg

    def test_malformed_json_uses_fallback(self, tmp_path):
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("not json {{{", encoding="utf-8")
        loader = MessageLoader(messages_path=bad_file)
        assert loader.total_messages >= 1

    def test_empty_messages_list_uses_fallback(self):
        path = self._create_temp_messages([])
        # Empty list triggers fallback since we validate non-empty
        # Actually _create_temp_messages creates {"messages": []}, let's make a proper one
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8")
        json.dump({"messages": []}, tmp)
        tmp.close()
        loader = MessageLoader(messages_path=Path(tmp.name))
        assert loader.total_messages >= 1

    def test_message_with_unescaped_braces_does_not_crash(self):
        path = self._create_temp_messages(["Hello {world} and {minutes}!"])
        loader = MessageLoader(messages_path=path)
        # Should not raise - uses str.replace instead of .format()
        msg = loader.get_message(minutes=10)
        assert "10" in msg


class TestNotifier:
    @patch("src.notifications.notifier.notification.notify")
    def test_send_calls_plyer(self, mock_notify):
        notifier = Notifier(title="Test Title")
        result = notifier.send("Test message")
        assert result is True
        mock_notify.assert_called_once_with(
            title="Test Title",
            message="Test message",
            app_name="IntelligentReminder",
            timeout=10,
        )

    @patch("src.notifications.notifier.notification.notify")
    def test_send_with_default_title(self, mock_notify):
        notifier = Notifier()
        notifier.send("Hello")
        call_kwargs = mock_notify.call_args[1]
        assert "Hidratação" in call_kwargs["title"]

    @patch("src.notifications.notifier.notification.notify")
    def test_send_unicode_message(self, mock_notify):
        notifier = Notifier()
        notifier.send("🥤 Bebe água! Está calor 🌡️")
        mock_notify.assert_called_once()

    @patch("src.notifications.notifier.notification.notify")
    def test_send_returns_false_on_exception(self, mock_notify):
        mock_notify.side_effect = RuntimeError("Notification service unavailable")
        notifier = Notifier()
        result = notifier.send("Test")
        assert result is False
