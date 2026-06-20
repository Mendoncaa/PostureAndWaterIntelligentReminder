import time
import threading
from unittest.mock import patch, MagicMock
import pytest

from src.main import IntelligentReminder


class TestIntegration:
    """Integration tests with accelerated timers."""

    def _fast_settings(self):
        return {
            "activity_threshold_minutes": 0.05,  # 3 seconds
            "idle_reset_minutes": 0.05,  # 3 seconds
            "notification_title": "Test Alert",
            "enabled": True,
        }

    @patch("src.notifications.notifier.notification.notify")
    @patch("src.monitor.activity_tracker.keyboard.Listener")
    @patch("src.monitor.activity_tracker.mouse.Listener")
    def test_notification_after_threshold(self, mock_mouse, mock_kb, mock_notify):
        """Continuous activity beyond threshold triggers notification."""
        settings = self._fast_settings()
        reminder = IntelligentReminder(settings=settings)

        # Override check interval to be fast
        reminder._check_timer = None

        reminder.start()

        # Simulate activity
        reminder._on_activity()
        time.sleep(0.5)

        # Manually trigger threshold check after enough time
        reminder._session_start = time.time() - 5  # Fake 5s of activity (threshold is 3s)
        reminder._notification_sent = False
        reminder._check_threshold()

        time.sleep(0.2)
        reminder.stop()

        mock_notify.assert_called_once()

    @patch("src.notifications.notifier.notification.notify")
    @patch("src.monitor.activity_tracker.keyboard.Listener")
    @patch("src.monitor.activity_tracker.mouse.Listener")
    def test_idle_resets_session(self, mock_mouse, mock_kb, mock_notify):
        """Idle period resets session start, preventing notification."""
        settings = self._fast_settings()
        reminder = IntelligentReminder(settings=settings)

        reminder.start()

        # Start a session
        reminder._on_activity()
        assert reminder._session_start is not None

        # Simulate idle reset
        reminder._on_idle_reset()
        assert reminder._session_start is None

        reminder.stop()
        mock_notify.assert_not_called()

    @patch("src.notifications.notifier.notification.notify")
    @patch("src.monitor.activity_tracker.keyboard.Listener")
    @patch("src.monitor.activity_tracker.mouse.Listener")
    def test_disabled_does_not_start(self, mock_mouse, mock_kb, mock_notify):
        """When disabled in config, nothing starts."""
        settings = self._fast_settings()
        settings["enabled"] = False
        reminder = IntelligentReminder(settings=settings)

        reminder.start()
        assert not reminder.is_running
        mock_kb.assert_not_called()

    @patch("src.notifications.notifier.notification.notify")
    @patch("src.monitor.activity_tracker.keyboard.Listener")
    @patch("src.monitor.activity_tracker.mouse.Listener")
    def test_graceful_shutdown(self, mock_mouse, mock_kb, mock_notify):
        """Stop cleans up all resources."""
        settings = self._fast_settings()
        reminder = IntelligentReminder(settings=settings)

        reminder.start()
        assert reminder.is_running

        reminder.stop()
        assert not reminder.is_running
        mock_kb.return_value.stop.assert_called_once()
        mock_mouse.return_value.stop.assert_called_once()

    @patch("src.notifications.notifier.notification.notify")
    @patch("src.monitor.activity_tracker.keyboard.Listener")
    @patch("src.monitor.activity_tracker.mouse.Listener")
    def test_notification_resets_session(self, mock_mouse, mock_kb, mock_notify):
        """After notification is sent, session resets for next cycle."""
        settings = self._fast_settings()
        reminder = IntelligentReminder(settings=settings)

        reminder.start()

        # Simulate past threshold
        reminder._session_start = time.time() - 10
        reminder._notification_sent = False
        reminder._check_threshold()

        time.sleep(0.2)

        # Session should be reset after notification
        assert reminder._session_start is None

        reminder.stop()
        mock_notify.assert_called_once()
