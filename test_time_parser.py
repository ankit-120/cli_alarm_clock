from datetime import datetime

import pytest

from time_parser import parse_time

NOW = datetime(2026, 9, 17, 9, 0, 0)


def test_duration_minutes():
    assert parse_time("10m", NOW) == datetime(2026, 9, 17, 9, 10, 0)


def test_duration_hours_and_minutes():
    assert parse_time("1h30m", NOW) == datetime(2026, 9, 17, 10, 30, 0)


def test_duration_seconds():
    assert parse_time("90s", NOW) == datetime(2026, 9, 17, 9, 1, 30)


def test_duration_combined_all_units():
    assert parse_time("1h2m3s", NOW) == datetime(2026, 9, 17, 10, 2, 3)


def test_absolute_time_later_today():
    assert parse_time("14:30", NOW) == datetime(2026, 9, 17, 14, 30, 0)


def test_absolute_time_earlier_today_rolls_to_tomorrow():
    assert parse_time("08:00", NOW) == datetime(2026, 9, 18, 8, 0, 0)


def test_absolute_time_equal_to_now_rolls_to_tomorrow():
    assert parse_time("09:00", NOW) == datetime(2026, 9, 18, 9, 0, 0)


def test_midnight():
    assert parse_time("00:00", NOW) == datetime(2026, 9, 18, 0, 0, 0)


def test_invalid_format_raises():
    with pytest.raises(ValueError):
        parse_time("not-a-time", NOW)


def test_invalid_hour_raises():
    with pytest.raises(ValueError):
        parse_time("24:00", NOW)


def test_empty_string_raises():
    with pytest.raises(ValueError):
        parse_time("", NOW)


def test_zero_duration_is_valid_and_immediate():
    assert parse_time("0s", NOW) == NOW
