from plyer import notification


class Notifier:
    """Sends native OS notifications."""

    def __init__(self, title: str = "🥤 Alerta de Hidratação & Postura"):
        self._title = title

    def send(self, message: str):
        """Send a native OS notification."""
        notification.notify(
            title=self._title,
            message=message,
            app_name="IntelligentReminder",
            timeout=10,
        )
