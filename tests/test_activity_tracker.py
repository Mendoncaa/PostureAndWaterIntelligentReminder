import time
from unittest.mock import MagicMock, patch
import pytest

from src.monitor.activity_tracker import ActivityTracker


class TestActivityTracker:
    def test_initial_state(self):
        tracker = ActivityTracker()
        assert not tracker.is_running
        assert tracker.last_activity_time <= time.time()

    def test_record_activity_updates_timestamp(self):
        tracker = ActivityTracker()
        old_time = tracker.last_activity_time
        time.sleep(0.05)
        tracker._record_activity()
        assert tracker.last_activity_time > old_time

    def test_callback_called_on_activity(self):
        callback = MagicMock()
        tracker = ActivityTracker(on_activity_callback=callback)
        tracker._record_activity()
        callback.assert_called_once()

    def test_key_event_records_activity(self):
        callback = MagicMock()
        tracker = ActivityTracker(on_activity_callback=callback)
        tracker._on_key_event(None)
        callback.assert_called_once()

    def test_mouse_move_records_activity(self):
        callback = MagicMock()
        tracker = ActivityTracker(on_activity_callback=callback)
        tracker._on_mouse_move(100, 200)
        callback.assert_called_once()

    def test_mouse_click_records_activity(self):
        callback = MagicMock()
        tracker = ActivityTracker(on_activity_callback=callback)
        tracker._on_mouse_click(100, 200, None, True)
        callback.assert_called_once()

    def test_mouse_scroll_records_activity(self):
        callback = MagicMock()
        tracker = ActivityTracker(on_activity_callback=callback)
        tracker._on_mouse_scroll(100, 200, 0, -3)
        callback.assert_called_once()

    @patch("src.monitor.activity_tracker.keyboard.Listener")
    @patch("src.monitor.activity_tracker.mouse.Listener")
    def test_start_creates_listeners(self, mock_mouse_listener, mock_keyboard_listener):
        tracker = ActivityTracker()
        tracker.start()
        assert tracker.is_running
        mock_keyboard_listener.return_value.start.assert_called_once()
        mock_mouse_listener.return_value.start.assert_called_once()
        tracker.stop()

    @patch("src.monitor.activity_tracker.keyboard.Listener")
    @patch("src.monitor.activity_tracker.mouse.Listener")
    def test_stop_cleans_up(self, mock_mouse_listener, mock_keyboard_listener):
        tracker = ActivityTracker()
        tracker.start()
        tracker.stop()
        assert not tracker.is_running
        mock_keyboard_listener.return_value.stop.assert_called_once()
        mock_mouse_listener.return_value.stop.assert_called_once()

    @patch("src.monitor.activity_tracker.keyboard.Listener")
    @patch("src.monitor.activity_tracker.mouse.Listener")
    def test_double_start_is_noop(self, mock_mouse_listener, mock_keyboard_listener):
        tracker = ActivityTracker()
        tracker.start()
        tracker.start()  # Should not create new listeners
        assert mock_keyboard_listener.call_count == 1
        tracker.stop()

    def test_thread_safety(self):
        """Concurrent access to last_activity_time should not raise."""
        tracker = ActivityTracker()
        import threading

        errors = []

        def writer():
            for _ in range(100):
                try:
                    tracker._record_activity()
                except Exception as e:
                    errors.append(e)

        def reader():
            for _ in range(100):
                try:
                    _ = tracker.last_activity_time
                except Exception as e:
                    errors.append(e)

        threads = [threading.Thread(target=writer), threading.Thread(target=reader)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0
