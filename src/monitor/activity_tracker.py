import time
import threading
from pynput import keyboard, mouse


class ActivityTracker:
    """Tracks keyboard and mouse activity using OS-level event hooks."""

    def __init__(self, on_activity_callback=None):
        self._on_activity = on_activity_callback
        self._last_activity_time = time.time()
        self._lock = threading.Lock()
        self._keyboard_listener = None
        self._mouse_listener = None
        self._running = False

    @property
    def last_activity_time(self) -> float:
        with self._lock:
            return self._last_activity_time

    def _record_activity(self):
        with self._lock:
            self._last_activity_time = time.time()
        if self._on_activity:
            self._on_activity()

    def _on_key_event(self, key):
        self._record_activity()

    def _on_mouse_move(self, x, y):
        self._record_activity()

    def _on_mouse_click(self, x, y, button, pressed):
        self._record_activity()

    def _on_mouse_scroll(self, x, y, dx, dy):
        self._record_activity()

    def start(self):
        if self._running:
            return

        self._running = True
        self._last_activity_time = time.time()

        self._keyboard_listener = keyboard.Listener(
            on_press=self._on_key_event,
            on_release=self._on_key_event,
        )
        self._mouse_listener = mouse.Listener(
            on_move=self._on_mouse_move,
            on_click=self._on_mouse_click,
            on_scroll=self._on_mouse_scroll,
        )

        self._keyboard_listener.start()
        self._mouse_listener.start()

    def stop(self):
        self._running = False
        if self._keyboard_listener:
            self._keyboard_listener.stop()
            self._keyboard_listener = None
        if self._mouse_listener:
            self._mouse_listener.stop()
            self._mouse_listener = None

    @property
    def is_running(self) -> bool:
        return self._running
