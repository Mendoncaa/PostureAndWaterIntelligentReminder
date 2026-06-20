import threading
import logging
from PIL import Image, ImageDraw
import pystray

logger = logging.getLogger(__name__)


def _create_icon_image(color: str = "#4FC3F7") -> Image.Image:
    """Generate a simple water drop icon programmatically."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Draw a filled circle (water drop simplified)
    draw.ellipse([12, 16, 52, 56], fill=color, outline="#0288D1")
    # Small triangle top (drop shape)
    draw.polygon([(32, 8), (22, 24), (42, 24)], fill=color, outline="#0288D1")
    return img


class TrayIcon:
    """System tray icon with pause/resume/quit controls."""

    def __init__(self, on_pause=None, on_resume=None, on_quit=None):
        self._on_pause = on_pause
        self._on_resume = on_resume
        self._on_quit = on_quit
        self._icon = None
        self._thread = None
        self._paused = False

    def _toggle_pause(self, icon, item):
        if self._paused:
            self._paused = False
            if self._on_resume:
                self._on_resume()
            self._update_menu()
        else:
            self._paused = True
            if self._on_pause:
                self._on_pause()
            self._update_menu()

    def _quit(self, icon, item):
        if self._on_quit:
            self._on_quit()
        # on_quit already calls stop() which stops the icon
        # Only stop directly if no callback was set
        if not self._on_quit:
            icon.stop()

    def _build_menu(self):
        pause_text = "▶ Retomar" if self._paused else "⏸ Pausar"
        return pystray.Menu(
            pystray.MenuItem(pause_text, self._toggle_pause),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("❌ Sair", self._quit),
        )

    def _update_menu(self):
        if self._icon:
            self._icon.menu = self._build_menu()
            color = "#9E9E9E" if self._paused else "#4FC3F7"
            self._icon.icon = _create_icon_image(color)
            self._icon.title = (
                "IntelligentReminder - Pausado" if self._paused
                else "IntelligentReminder - Ativo"
            )

    def start(self):
        """Start tray icon in a background thread."""
        self._icon = pystray.Icon(
            name="IntelligentReminder",
            icon=_create_icon_image(),
            title="IntelligentReminder - Ativo",
            menu=self._build_menu(),
        )
        self._thread = threading.Thread(target=self._icon.run, daemon=True)
        self._thread.start()
        logger.info("System tray icon ativo")

    def stop(self):
        """Stop tray icon."""
        if self._icon:
            self._icon.stop()
            self._icon = None

    @property
    def is_paused(self) -> bool:
        return self._paused
