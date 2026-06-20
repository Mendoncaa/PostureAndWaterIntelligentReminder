import signal
import sys
import time
import threading

from src.config.settings import load_settings, get_activity_threshold_seconds, get_idle_reset_seconds
from src.monitor.activity_tracker import ActivityTracker
from src.monitor.idle_detector import IdleDetector
from src.notifications.messages import MessageLoader
from src.notifications.notifier import Notifier


class IntelligentReminder:
    """Main orchestrator: monitors activity and sends hydration/posture reminders."""

    def __init__(self, settings: dict = None):
        self._settings = settings or load_settings()
        self._activity_threshold = get_activity_threshold_seconds(self._settings)
        self._idle_reset = get_idle_reset_seconds(self._settings)

        self._tracker = ActivityTracker(on_activity_callback=self._on_activity)
        self._idle_detector = IdleDetector(
            idle_threshold_seconds=self._idle_reset,
            on_idle_callback=self._on_idle_reset,
        )
        self._message_loader = MessageLoader()
        self._notifier = Notifier(title=self._settings["notification_title"])

        self._session_start = None
        self._notification_sent = False
        self._check_timer = None
        self._running = False
        self._lock = threading.Lock()

    def _on_activity(self):
        """Called on every keyboard/mouse event."""
        with self._lock:
            if self._session_start is None:
                self._session_start = time.time()
                self._notification_sent = False

    def _on_idle_reset(self):
        """Called when user is idle long enough to reset the timer."""
        with self._lock:
            self._session_start = None
            self._notification_sent = False

    def _check_threshold(self):
        """Periodically check if activity threshold has been reached."""
        if not self._running:
            return

        with self._lock:
            if (
                self._session_start is not None
                and not self._notification_sent
            ):
                elapsed = time.time() - self._session_start
                if elapsed >= self._activity_threshold:
                    minutes = int(elapsed / 60)
                    message = self._message_loader.get_message(minutes=minutes)
                    self._notifier.send(message)
                    self._notification_sent = True
                    # Reset session so it can trigger again after next idle+active cycle
                    self._session_start = None

        # Schedule next check (every 30 seconds)
        if self._running:
            self._check_timer = threading.Timer(30, self._check_threshold)
            self._check_timer.daemon = True
            self._check_timer.start()

    def start(self):
        """Start monitoring."""
        if not self._settings["enabled"]:
            print("IntelligentReminder está desativado na configuração.")
            return

        self._running = True
        self._session_start = None
        self._notification_sent = False

        # Start activity tracker
        self._tracker.start()

        # Connect idle detector to tracker
        self._idle_detector.set_activity_source(lambda: self._tracker.last_activity_time)
        self._idle_detector.start()

        # Start threshold checker
        self._check_threshold()

        minutes = self._settings["activity_threshold_minutes"]
        idle_min = self._settings["idle_reset_minutes"]
        print(f"✅ IntelligentReminder ativo!")
        print(f"   ⏱️  Alerta após {minutes} min de atividade contínua")
        print(f"   😴 Reset após {idle_min} min de inatividade")
        print(f"   📝 {self._message_loader.total_messages} mensagens carregadas")
        print(f"   Ctrl+C para sair")

    def stop(self):
        """Stop all monitoring and clean up."""
        self._running = False

        if self._check_timer:
            self._check_timer.cancel()
            self._check_timer = None

        self._idle_detector.stop()
        self._tracker.stop()
        print("\n🛑 IntelligentReminder encerrado. Até à próxima!")

    @property
    def is_running(self) -> bool:
        return self._running


def main():
    settings = load_settings()
    reminder = IntelligentReminder(settings=settings)

    def signal_handler(signum, frame):
        reminder.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    reminder.start()

    # Keep main thread alive
    try:
        while reminder.is_running:
            time.sleep(1)
    except KeyboardInterrupt:
        reminder.stop()


if __name__ == "__main__":
    main()
