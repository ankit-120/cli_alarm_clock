import re
from datetime import datetime, timedelta

DURATION_RE = re.compile(r"^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$", re.IGNORECASE)


def parse_time(value: str, now: datetime) -> datetime:
    """Resolve a user-supplied time string to an absolute datetime.

    Accepts either a duration (e.g. "10m", "1h30m", "90s") relative to `now`,
    or an absolute 24h clock time "HH:MM", which resolves to the next
    occurrence of that time (today if still ahead, otherwise tomorrow).

    `now` is injected rather than read internally so this function is a pure,
    deterministic unit to test.
    """
    match = DURATION_RE.match(value)
    if match and any(match.groups()):
        hours, minutes, seconds = (int(g) if g else 0 for g in match.groups())
        return now + timedelta(hours=hours, minutes=minutes, seconds=seconds)

    try:
        target = datetime.strptime(value, "%H:%M")
    except ValueError:
        raise ValueError(
            f"Unrecognized time format: {value!r}. Use HH:MM or a duration like 10m, 1h30m, 90s."
        )

    target = target.replace(year=now.year, month=now.month, day=now.day)
    if target <= now:
        target += timedelta(days=1)
    return target
