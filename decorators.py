"""Decorators: logging and execution-time measurement."""

import functools
import time
from datetime import datetime


def log_call(func):
    """Log every call of the wrapped function with its outcome."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        stamp = datetime.now().strftime("%H:%M:%S")
        print(f"[LOG {stamp}] -> {func.__qualname__}")
        try:
            result = func(*args, **kwargs)
        except Exception as exc:
            print(f"[LOG {stamp}] !! {func.__qualname__} failed: {exc}")
            raise
        print(f"[LOG {stamp}] <- {func.__qualname__} OK")
        return result

    return wrapper


def timed(func):
    """Measure and print how long the wrapped function takes."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            print(f"[TIME] {func.__qualname__} took {elapsed_ms:.3f} ms")

    return wrapper
