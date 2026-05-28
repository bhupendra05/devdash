"""Weather widget — uses wttr.in (free, no API key)."""
from __future__ import annotations
import json
import urllib.request
import urllib.error
from dataclasses import dataclass
from typing import Optional


@dataclass
class WeatherData:
    location: str
    temp_c: float
    feels_like_c: float
    condition: str
    humidity: int
    icon: str


_CONDITION_ICONS = {
    "sunny": "☀️", "clear": "🌙", "partly cloudy": "⛅", "cloudy": "☁️",
    "overcast": "☁️", "rain": "🌧️", "drizzle": "🌦️", "snow": "❄️",
    "thunder": "⛈️", "fog": "🌫️", "mist": "🌫️", "wind": "💨",
}


def _pick_icon(condition: str) -> str:
    c = condition.lower()
    for kw, icon in _CONDITION_ICONS.items():
        if kw in c:
            return icon
    return "🌡️"


def fetch_weather(location: str = "", timeout: int = 5) -> Optional[WeatherData]:
    """Fetch weather from wttr.in — free, no API key needed."""
    loc = location.replace(" ", "+") if location else ""
    url = f"https://wttr.in/{loc}?format=j1"
    req = urllib.request.Request(url, headers={"User-Agent": "devdash/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
    except Exception:
        return None

    try:
        current = data["current_condition"][0]
        area = data["nearest_area"][0]
        city = area["areaName"][0]["value"]
        country = area["country"][0]["value"]
        condition = current["weatherDesc"][0]["value"]
        return WeatherData(
            location=f"{city}, {country}",
            temp_c=float(current["temp_C"]),
            feels_like_c=float(current["FeelsLikeC"]),
            condition=condition,
            humidity=int(current["humidity"]),
            icon=_pick_icon(condition),
        )
    except (KeyError, IndexError, ValueError):
        return None
