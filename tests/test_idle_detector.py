import time
from unittest.mock import MagicMock
import pytest

from src.monitor.idle_detector import IdleDetector


class TestIdleDetector:
    def test_initial_state(self):
        detector = IdleDetector(idle_threshold_seconds=300)
        assert not detector.is_running
        assert not detector.is_idle_triggered

    def test_idle_triggers_callback_when_threshold_reached(self):
        callback = MagicMock()
        detector = IdleDetector(idle_threshold_seconds=1, on_idle_callback=callback)
        detector._check_interval = 0.1

        # Simulate last activity 2 seconds ago
        last_activity = time.time() - 2
        detector.set_activity_source(lambda: last_activity)

        detector.start()
        time.sleep(0.3)
        detector.stop()

        callback.assert_called()

    def test_no_idle_when_recently_active(self):
        callback = MagicMock()
        detector = IdleDetector(idle_threshold_seconds=300, on_idle_callback=callback)
        detector._check_interval = 0.1

        # Simulate very recent activity
        detector.set_activity_source(lambda: time.time())

        detector.start()
        time.sleep(0.3)
        detector.stop()

        callback.assert_not_called()

    def test_idle_resets_when_activity_resumes(self):
        callback = MagicMock()
        detector = IdleDetector(idle_threshold_seconds=1, on_idle_callback=callback)
        detector._check_interval = 0.1

        # Start idle
        idle_time = time.time() - 2
        activity_time = [idle_time]
        detector.set_activity_source(lambda: activity_time[0])

        detector.start()
        time.sleep(0.3)

        # Simulate activity resuming
        activity_time[0] = time.time()
        time.sleep(0.3)

        # idle_triggered should be False now
        assert not detector.is_idle_triggered
        detector.stop()

    def test_stop_cancels_timer(self):
        detector = IdleDetector(idle_threshold_seconds=300)
        detector.set_activity_source(lambda: time.time())
        detector.start()
        assert detector.is_running
        detector.stop()
        assert not detector.is_running

    def test_idle_callback_only_fires_once_per_idle_period(self):
        callback = MagicMock()
        detector = IdleDetector(idle_threshold_seconds=1, on_idle_callback=callback)
        detector._check_interval = 0.1

        # Simulate last activity 5 seconds ago
        old_time = time.time() - 5
        detector.set_activity_source(lambda: old_time)

        detector.start()
        time.sleep(0.5)  # Multiple check cycles
        detector.stop()

        # Should only fire once per idle period
        callback.assert_called_once()
