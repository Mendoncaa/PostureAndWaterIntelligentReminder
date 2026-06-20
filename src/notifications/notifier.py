import logging
from plyer import notification

logger = logging.getLogger(__name__)


class Notifier:
    """Sends native OS notifications."""

    def __init__(self, title: str = "🥤 Alerta de Hidratação & Postura"):
        self._title = title

    def send(self, message: str) -> bool:
        """Send a native OS notification. Returns True if successful."""
        try:
            notification.notify(
                title=self._title,
                message=message,
                app_name="IntelligentReminder",
                timeout=10,
            )
            return True
        except Exception as e:
            logger.error(f"Falha ao enviar notificação: {e}")
            return False
