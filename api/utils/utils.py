from datetime import datetime, timedelta, timezone


def expiration_midnight() -> int:
    now = datetime.now(timezone.utc)
    midnight = (now + timedelta(1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return int((midnight - now).total_seconds())
