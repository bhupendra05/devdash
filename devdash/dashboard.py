"""Main dashboard renderer using Rich."""
from __future__ import annotations
import time
from typing import Optional

from rich.columns import Columns
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from .widgets.clock import render_clock
from .widgets.system import get_system_stats, format_stats
from .widgets.weather import fetch_weather, WeatherData
from .widgets.github import fetch_github, GitHubStats
from .widgets.quotes import quote_of_the_day


console = Console()


def _clock_panel(data: dict) -> Panel:
    t = Text()
    t.append(f"\n {data['icon']}  {data['greeting']}!\n\n", style="bold yellow")
    t.append(f"  🕐  {data['time']}\n", style="bold cyan")
    t.append(f"  📅  {data['date']}\n", style="dim")
    return Panel(t, title="[bold]Time[/bold]", border_style="cyan", box=box.ROUNDED)


def _system_panel() -> Panel:
    stats = get_system_stats()
    lines = format_stats(stats)
    t = Text("\n")
    for line in lines:
        # colour the bar based on usage
        if "CPU" in line:
            pct = stats.cpu_percent
        elif "RAM" in line:
            pct = stats.mem_percent
        else:
            pct = stats.disk_percent

        colour = "green" if pct < 60 else "yellow" if pct < 85 else "red"
        t.append(f"  {line}\n", style=colour)
    t.append(f"\n  💻 {stats.platform}\n", style="dim")
    return Panel(t, title="[bold]System[/bold]", border_style="blue", box=box.ROUNDED)


def _weather_panel(weather: Optional[WeatherData]) -> Panel:
    if weather is None:
        t = Text("\n  🌐 No connection\n  (weather unavailable)\n", style="dim")
    else:
        t = Text()
        t.append(f"\n  {weather.icon}  {weather.condition}\n", style="bold")
        t.append(f"  🌡️  {weather.temp_c:.0f}°C", style="yellow")
        t.append(f"  (feels {weather.feels_like_c:.0f}°C)\n", style="dim")
        t.append(f"  💧 Humidity: {weather.humidity}%\n", style="cyan")
        t.append(f"  📍 {weather.location}\n", style="dim")
    return Panel(t, title="[bold]Weather[/bold]", border_style="yellow", box=box.ROUNDED)


def _github_panel(gh: Optional[GitHubStats]) -> Panel:
    if gh is None:
        t = Text("\n  🐙 Not configured\n  Run: devdash --github YOUR_USERNAME\n", style="dim")
    else:
        t = Text()
        t.append(f"\n  🐙 @{gh.username}\n", style="bold green")
        if gh.bio:
            t.append(f"  {gh.bio[:45]}\n", style="dim italic")
        t.append(f"\n  📦 {gh.repos} repos\n", style="cyan")
        t.append(f"  👥 {gh.followers} followers · {gh.following} following\n", style="dim")
    return Panel(t, title="[bold]GitHub[/bold]", border_style="green", box=box.ROUNDED)


def _quote_panel() -> Panel:
    quote, author = quote_of_the_day()
    # Word-wrap manually to ~60 chars
    words = quote.split()
    lines, current = [], ""
    for w in words:
        if len(current) + len(w) + 1 > 58:
            lines.append(current)
            current = w
        else:
            current = (current + " " + w).strip()
    if current:
        lines.append(current)

    t = Text("\n")
    for line in lines:
        t.append(f"  {line}\n", style="italic")
    t.append(f"\n    — {author}\n", style="bold dim")
    return Panel(t, title="[bold]Quote of the Day[/bold]", border_style="magenta", box=box.ROUNDED)


def build_layout(weather, gh) -> Table:
    """Build the full dashboard layout."""
    clock_data = render_clock()

    root = Table.grid(padding=0)
    root.add_column()

    # Row 1: clock + weather + github
    top = Columns([
        _clock_panel(clock_data),
        _weather_panel(weather),
        _github_panel(gh),
    ], equal=True, expand=True)
    root.add_row(top)

    # Row 2: system + quote
    bot = Columns([
        _system_panel(),
        _quote_panel(),
    ], equal=True, expand=True)
    root.add_row(bot)

    return root


def run_dashboard(
    github_username: str = "",
    location: str = "",
    refresh: float = 2.0,
    once: bool = False,
) -> None:
    """Run the live dashboard."""
    console.print("[dim]devdash — loading widgets...[/dim]")

    # Fetch slow data once (weather + github change rarely)
    weather = fetch_weather(location)
    gh = fetch_github(github_username) if github_username else None

    if once:
        console.print(build_layout(weather, gh))
        return

    refresh_weather_every = 300  # seconds
    refresh_gh_every = 120
    last_weather = last_gh = time.time()

    with Live(build_layout(weather, gh), console=console,
              refresh_per_second=1 / refresh, screen=True) as live:
        try:
            while True:
                now = time.time()
                if now - last_weather > refresh_weather_every:
                    weather = fetch_weather(location)
                    last_weather = now
                if github_username and now - last_gh > refresh_gh_every:
                    gh = fetch_github(github_username)
                    last_gh = now
                live.update(build_layout(weather, gh))
                time.sleep(refresh)
        except KeyboardInterrupt:
            pass
