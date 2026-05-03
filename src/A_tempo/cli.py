"""tempo - Print current local time and day of week.

Usage:
    A tempo           # Show current local time
    A tempo -z       # Show all UTC offsets
    A tempo --horzono 9  # Show time for UTC+9
"""

from __future__ import annotations

import datetime
from typing import Optional

import typer

from A.utils import info
from A.core.i18n import tr_multi

app = typer.Typer(
    name="tempo",
    help=tr_multi("Presi aktualan lokan tempon kaj semajntagon", "Print current local time and day of week", "Imprimer l'heure locale actuelle et le jour de la semaine"),
    invoke_without_command=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)

UTC_MIN = -12
UTC_MAX = 14

# Cache for day names to avoid repeated locale calls
_day_names_cache: dict[str, str] = {}


def _get_timezone(offset: int) -> datetime.timezone:
    """Get timezone for given UTC offset."""
    return datetime.timezone(datetime.timedelta(hours=offset))


def _time_for_offset(offset: int) -> datetime.datetime:
    """Get current time for given UTC offset."""
    return datetime.datetime.now(tz=_get_timezone(offset))


def _day_name(dt: datetime.datetime) -> str:
    """Return localized day-of-week name using system locale."""
    # Use str() of tzinfo as cache key (works for all tz types)
    tz_key = str(dt.tzinfo) if dt.tzinfo else "local"

    if tz_key in _day_names_cache:
        return _day_names_cache[tz_key]

    try:
        import locale

        locale.setlocale(locale.LC_TIME, "")
        name = dt.strftime("%A")
    except locale.Error:
        # Fallback to English day names
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        name = days[dt.weekday()]

    _day_names_cache[tz_key] = name
    return name


@app.callback(invoke_without_command=True)
def tempo(
    ctx: typer.Context,
    horzono: Optional[int] = typer.Option(
        None,
        "-z",
        "--horzono",
        help=tr_multi("UTC horzona offset (-12 al +14)", "UTC timezone offset (-12 to +14)", "Décalage fuseau horaire UTC (-12 à +14)"),
    ),
    chiuj: bool = typer.Option(
        False,
        "-a",
        "--chiuj-horzonoj",
        help=tr_multi("Montri ĉiujn UTC-offsetojn (-12 al +14)", "Show all UTC offsets (-12 to +14)", "Afficher tous les décalages UTC (-12 à +14)"),
    ),
) -> None:
    """Print current local time (ISO 8601) and day of week."""
    if ctx.invoked_subcommand is not None:
        return

    if chiuj:
        lines = []
        for offset in range(UTC_MIN, UTC_MAX + 1):
            dt = _time_for_offset(offset)
            utcoff = dt.utcoffset()
            prefix = f"UTC{utcoff.total_seconds() / 3600:+g}  " if utcoff else ""
            lines.append(f"{prefix}{dt.isoformat(timespec='seconds')}")
        info("\n".join(lines))
        return

    if horzono is not None:
        if not UTC_MIN <= horzono <= UTC_MAX:
            raise typer.BadParameter(f"horzono must be between {UTC_MIN} and {UTC_MAX}")
        dt = _time_for_offset(horzono)
        info(f"{dt.isoformat(timespec='seconds')}\n{_day_name(dt)}")
        return

    # Default: local system time
    now = datetime.datetime.now().astimezone()
    info(f"{now.isoformat(timespec='seconds')}\n{_day_name(now)}")


__all__ = ["app"]