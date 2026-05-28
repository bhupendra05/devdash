"""Tests for devdash widgets."""
import pytest
from datetime import date
from devdash.widgets.clock import render_clock, get_greeting
from devdash.widgets.system import get_system_stats, format_stats, _bar
from devdash.widgets.weather import WeatherData, _pick_icon
from devdash.widgets.github import GitHubStats
from devdash.widgets.quotes import quote_of_the_day, QUOTES


# ---------------------------------------------------------------------------
# Clock widget
# ---------------------------------------------------------------------------

class TestClock:
    def test_render_clock_returns_dict(self):
        result = render_clock()
        assert isinstance(result, dict)

    def test_render_clock_has_required_keys(self):
        result = render_clock()
        for key in ("time", "date", "greeting", "icon"):
            assert key in result

    def test_time_format(self):
        result = render_clock()
        parts = result["time"].split(":")
        assert len(parts) == 3
        assert all(p.isdigit() for p in parts)

    def test_greeting_is_string(self):
        _, greeting = get_greeting()
        assert isinstance(greeting, str)
        assert len(greeting) > 0

    def test_icon_is_string(self):
        icon, _ = get_greeting()
        assert isinstance(icon, str)


# ---------------------------------------------------------------------------
# System widget
# ---------------------------------------------------------------------------

class TestSystemStats:
    def test_get_stats_returns_object(self):
        s = get_system_stats()
        assert s is not None

    def test_cpu_in_range(self):
        s = get_system_stats()
        assert 0.0 <= s.cpu_percent <= 100.0

    def test_mem_positive(self):
        s = get_system_stats()
        assert s.mem_total_gb >= 0

    def test_disk_positive(self):
        s = get_system_stats()
        assert s.disk_total_gb > 0

    def test_format_stats_returns_three_lines(self):
        s = get_system_stats()
        lines = format_stats(s)
        assert len(lines) == 3

    def test_format_stats_strings(self):
        s = get_system_stats()
        for line in format_stats(s):
            assert isinstance(line, str)

    def test_bar_full(self):
        assert "░" not in _bar(100, 10)

    def test_bar_empty(self):
        assert "█" not in _bar(0, 10)

    def test_bar_half(self):
        b = _bar(50, 10)
        assert len(b) == 10

    def test_bar_width(self):
        for w in (5, 10, 20, 30):
            assert len(_bar(50, w)) == w


# ---------------------------------------------------------------------------
# Weather widget
# ---------------------------------------------------------------------------

class TestWeather:
    def test_pick_icon_sunny(self):
        assert _pick_icon("Sunny") == "☀️"

    def test_pick_icon_rain(self):
        assert _pick_icon("Heavy Rain") == "🌧️"

    def test_pick_icon_snow(self):
        assert _pick_icon("Light Snow") == "❄️"

    def test_pick_icon_unknown(self):
        result = _pick_icon("Bizarre alien weather")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_weather_dataclass(self):
        w = WeatherData(
            location="Mumbai, India",
            temp_c=32.0,
            feels_like_c=38.0,
            condition="Sunny",
            humidity=80,
            icon="☀️",
        )
        assert w.temp_c == 32.0
        assert w.humidity == 80


# ---------------------------------------------------------------------------
# GitHub widget
# ---------------------------------------------------------------------------

class TestGitHub:
    def test_github_stats_dataclass(self):
        g = GitHubStats(
            username="bhupendra05",
            repos=42,
            followers=100,
            following=50,
            bio="Builder",
        )
        assert g.username == "bhupendra05"
        assert g.repos == 42


# ---------------------------------------------------------------------------
# Quotes widget
# ---------------------------------------------------------------------------

class TestQuotes:
    def test_quote_returns_tuple(self):
        result = quote_of_the_day()
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_quote_strings(self):
        quote, author = quote_of_the_day()
        assert isinstance(quote, str)
        assert isinstance(author, str)
        assert len(quote) > 10
        assert len(author) > 2

    def test_quote_deterministic_same_day(self):
        q1 = quote_of_the_day()
        q2 = quote_of_the_day()
        assert q1 == q2

    def test_all_quotes_have_two_parts(self):
        for q in QUOTES:
            assert len(q) == 2
            text, author = q
            assert isinstance(text, str) and isinstance(author, str)

    def test_quotes_not_empty(self):
        assert len(QUOTES) >= 10
