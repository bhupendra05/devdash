"""CLI entry point for devdash."""
import click
from .dashboard import run_dashboard


@click.command()
@click.option("--github", "-g", default="", envvar="DEVDASH_GITHUB",
              help="GitHub username to show stats for.")
@click.option("--location", "-l", default="", envvar="DEVDASH_LOCATION",
              help="City for weather (e.g. 'London'). Auto-detected if omitted.")
@click.option("--refresh", "-r", default=2.0, show_default=True,
              help="Refresh interval in seconds.")
@click.option("--once", is_flag=True,
              help="Print once and exit (no live mode). Good for screenshots.")
def main(github: str, location: str, refresh: float, once: bool) -> None:
    """
    devdash — beautiful developer dashboard for your terminal.

    Shows clock, weather, GitHub stats, system usage, and quote of the day.
    Refreshes live every few seconds.

    \b
    Examples:
      devdash
      devdash --github bhupendra05
      devdash --github bhupendra05 --location Mumbai
      devdash --once   # print snapshot and exit
    """
    run_dashboard(
        github_username=github,
        location=location,
        refresh=refresh,
        once=once,
    )


if __name__ == "__main__":
    main()
