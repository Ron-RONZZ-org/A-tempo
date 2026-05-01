"""Tests for A-tempo."""

from __future__ import annotations

import datetime
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from A_tempo.cli import app, _day_name, _time_for_offset, UTC_MAX, UTC_MIN

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


class TestDayName:
    """Tests for _day_name()."""

    def test_returns_string(self):
        dt = datetime.datetime(2024, 1, 1, 12, 0, tzinfo=datetime.timezone.utc)
        result = _day_name(dt)
        assert isinstance(result, str)
        assert len(result) > 0


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