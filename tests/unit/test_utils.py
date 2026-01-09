from datetime import datetime

from src.utils import parse_iso8601


def test_parse_iso8601():
    date_str = "2023-01-01T12:00:00.000Z"
    result = parse_iso8601(date_str)
    assert isinstance(result, datetime)
    assert result.year == 2023
    assert result.month == 1
