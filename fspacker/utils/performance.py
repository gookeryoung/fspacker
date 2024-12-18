import logging
import time
from functools import wraps


def perf_timer(func):
    """Decorator function to test performance."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        logging.info(
            f"Function '{func.__name__}' took {elapsed_time:.5f}s to complete."
        )
        return result

    return wrapper
