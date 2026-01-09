from datetime import datetime


def parse_iso8601(date_str: str) -> datetime:
    return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
