import time
import threading


class IdleDetector:
    """Detects user inactivity and triggers reset when idle threshold is reached."""

    def __init__(self, idle_threshold_seconds: int, on_idle_callback=None):
        self._idle_threshold = idle_threshold_seconds
        self._on_idle = on_idle_callback
        self._check_interval = 10  # Check every 10 seconds
        self._timer = None
        self._running = False
        self._idle_triggered = False
        self._get_last_activity = None

    def set_activity_source(self, get_last_activity_func):
        """Set function that returns the timestamp of last activity."""
        self._get_last_activity = get_last_activity_func

    def _check_idle(self):
        if not self._running or not self._get_last_activity:
            return

        elapsed = time.time() - self._get_last_activity()

        if elapsed >= self._idle_threshold and not self._idle_triggered:
            self._idle_triggered = True
            if self._on_idle:
                self._on_idle()
        elif elapsed < self._idle_threshold:
            self._idle_triggered = False

        # Schedule next check
        if self._running:
            self._timer = threading.Timer(self._check_interval, self._check_idle)
            self._timer.daemon = True
            self._timer.start()

    def start(self):
        if self._running:
            return
        self._running = True
        self._idle_triggered = False
        self._check_idle()

    def stop(self):
        self._running = False
        if self._timer:
            self._timer.cancel()
            self._timer = None

    @property
    def is_idle_triggered(self) -> bool:
        return self._idle_triggered

    @property
    def is_running(self) -> bool:
        return self._running
