# app/utils/rate_limits.py

import time
from functools import wraps

_CALL_TIMES = {}


def rate_limit(key: str, seconds: int = 2):
    """
    Simple in-memory rate limiter.
    key = unique operation name
    seconds = cooldown
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            last_called = _CALL_TIMES.get(key, 0)

            if now - last_called < seconds:
                raise Exception(
                    f"Rate limit exceeded for '{key}'. Try again in {int(seconds - (now - last_called))}s."
                )

            _CALL_TIMES[key] = now
            return func(*args, **kwargs)

        return wrapper

    return decorator