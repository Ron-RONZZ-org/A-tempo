"""Tests for A-tempo."""

from __future__ import annotations

import datetime
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from A_tempo.cli import app, _day_name, _time_for_offset, _get_timezone, UTC_MAX, UTC_MIN

runner = CliRunner()


class TestTimeForOffset:
    """Tests for _time_for_offset()."""

    def test_returns_datetime_with_timezone(self):
        offset = 9
        result = _time_for_offset(offset)
        assert isinstance(result, datetime.datetime)
        assert result.tzinfo is not None

    def test_correct_offset(self):
        offset = 5
        result = _time_for_offset(offset)
        expected = datetime.timezone(datetime.timedelta(hours=offset))
        assert result.tzinfo == expected


class TestGetTimezone:
    """Tests for _get_timezone()."""

    def test_returns_timezone(self):
        result = _get_timezone(0)
        assert isinstance(result, datetime.timezone)

    def test_positive_offset(self):
        result = _get_timezone(5)
        expected = datetime.timezone(datetime.timedelta(hours=5))
        assert result == expected

    def test_negative_offset(self):
        result = _get_timezone(-8)
        expected = datetime.timezone(datetime.timedelta(hours=-8))
        assert result == expected

    def test_utc_min_offset(self):
        result = _get_timezone(UTC_MIN)
        expected = datetime.timezone(datetime.timedelta(hours=UTC_MIN))
        assert result == expected

    def test_utc_max_offset(self):
        result = _get_timezone(UTC_MAX)
        expected = datetime.timezone(datetime.timedelta(hours=UTC_MAX))
        assert result == expected


class TestDayName:
    """Tests for _day_name()."""

    def test_returns_string(self):
        dt = datetime.datetime(2024, 1, 1, 12, 0, tzinfo=datetime.timezone.utc)
        result = _day_name(dt)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_caching(self):
        """Test that _day_name caches results for same timezone."""
        import A_tempo.cli as cli_module

        # Clear cache first
        cli_module._day_names_cache.clear()

        dt1 = datetime.datetime(2024, 1, 1, 12, 0, tzinfo=datetime.timezone.utc)
        dt2 = datetime.datetime(2024, 1, 8, 12, 0, tzinfo=datetime.timezone.utc)  # Same weekday

        result1 = _day_name(dt1)
        cache_size_after_first = len(cli_module._day_names_cache)

        result2 = _day_name(dt2)
        cache_size_after_second = len(cli_module._day_names_cache)

        assert result1 == result2
        assert cache_size_after_second == cache_size_after_first  # No new cache entry


class TestTempo:
    """Tests for tempo CLI."""

    def test_default_local_time(self):
        result = runner.invoke(app, [])
        assert result.exit_code == 0
        assert "T" in result.stdout  # ISO format has T

    def test_specific_utc_offset(self):
        result = runner.invoke(app, ["--horzono", "9"])
        assert result.exit_code == 0
        assert "+09:00" in result.stdout  # ISO format shows offset

    def test_all_utc_offsets(self):
        result = runner.invoke(app, ["--chiuj-horzonoj"])
        assert result.exit_code == 0
        # Should show range from UTC-12 to UTC+14
        assert "UTC-12" in result.stdout
        assert "UTC+14" in result.stdout

    def test_invalid_offset(self):
        result = runner.invoke(app, ["--horzono", "99"])
        assert result.exit_code != 0
        assert "horzono" in result.output.lower() or "must be between" in result.output.lower()

    def test_negative_invalid_offset(self):
        result = runner.invoke(app, ["--horzono", "-99"])
        assert result.exit_code != 0

    def test_utc_min_boundary(self):
        result = runner.invoke(app, ["--horzono", str(UTC_MIN)])
        assert result.exit_code == 0
        assert f"UTC{UTC_MIN}" in result.stdout or f"{UTC_MIN:>+3}:00" in result.stdout

    def test_utc_max_boundary(self):
        result = runner.invoke(app, ["--horzono", str(UTC_MAX)])
        assert result.exit_code == 0
        assert f"UTC+{UTC_MAX}" in result.stdout or f"+{UTC_MAX:>2}:00" in result.stdout

    def test_help_flag(self):
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "tempo" in result.stdout.lower()