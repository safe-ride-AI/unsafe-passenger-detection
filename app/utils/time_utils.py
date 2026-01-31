from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def seconds_between(
    t1: datetime,
    t2: datetime
) -> float:
    return abs((t2 - t1).total_seconds())
