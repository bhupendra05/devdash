"""Clock and greeting widget."""
from datetime import datetime, timezone
import platform


_GREETINGS = {
    range(5, 12):  ("🌅", "Good morning"),
    range(12, 17): ("☀️", "Good afternoon"),
    range(17, 21): ("🌆", "Good evening"),
}


def get_greeting() -> tuple[str, str]:
    hour = datetime.now().hour
    for h_range, (icon, text) in _GREETINGS.items():
        if hour in h_range:
            return icon, text
    return "🌙", "Good night"


def render_clock() -> dict:
    now = datetime.now()
    icon, greeting = get_greeting()
    return {
        "time": now.strftime("%H:%M:%S"),
        "date": now.strftime("%A, %B %d %Y"),
        "greeting": greeting,
        "icon": icon,
    }
