import time
from collections import defaultdict

# Simple in-memory rate limiter
_CALL_LOG = defaultdict(list)

def rate_limit(
    key: str,
    max_calls: int,
    window_seconds: int
):
    """
    Prevents more than `max_calls` in `window_seconds`
    """
    now = time.time()
    calls = _CALL_LOG[key]

    # Remove expired calls
    _CALL_LOG[key] = [
        t for t in calls if now - t < window_seconds
    ]

    if len(_CALL_LOG[key]) >= max_calls:
        raise Exception(
            f"Rate limit exceeded: {max_calls} calls per {window_seconds}s"
        )

    _CALL_LOG[key].append(now)
