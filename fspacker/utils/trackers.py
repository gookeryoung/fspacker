import atexit
import logging
import os
import time
import typing
from functools import wraps
from threading import Lock

__all__ = [
    "perf_tracker",
]


class PerformanceTracker:
    """Performance tracker class."""

    global_start_time = None
    function_times: typing.Dict[str, float] = {}
    total_time = 0.0
    lock = Lock()
    debug_mode = False

    @classmethod
    def initialize(cls):
        if cls.global_start_time is None:
            cls.global_start_time = time.perf_counter()
            cls.function_times = {}
            cls.total_time = 0.0
            cls.debug_mode = os.getenv("DEBUG", "False").lower() in (
                "true",
                "1",
                "t",
            )

    @classmethod
    def update_total_time(cls):
        if cls.global_start_time is not None:
            cls.total_time = time.perf_counter() - cls.global_start_time

    @classmethod
    def finalize(cls):
        if cls.global_start_time is not None and cls.debug_mode:
            cls.update_total_time()
            logging.debug(
                f"{'-' * 20}Summary{'-' * 20}\n[*] Total application runtime: {cls.total_time:.6f} seconds."
            )
            for func_name, elapsed_time in cls.function_times.items():
                percentage = (
                    (elapsed_time / cls.total_time) * 100 if cls.total_time > 0 else 0
                )
                logging.debug(
                    f"Function '{func_name}' total time: {elapsed_time:.6f} seconds [{percentage:.2f}% of total]."
                )
            cls.global_start_time = None


def perf_tracker(func):
    """Decorator function to test performance."""

    PerformanceTracker.initialize()

    @wraps(func)
    def wrapper(*args, **kwargs):
        if PerformanceTracker.debug_mode:
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time

            with PerformanceTracker.lock:
                func_name = f"{func.__module__}.{func.__name__}"
                PerformanceTracker.function_times[func_name] = (
                    PerformanceTracker.function_times.get(func_name, 0) + elapsed_time
                )

            PerformanceTracker.update_total_time()
            total_time = PerformanceTracker.total_time
            if total_time > 0:
                percentage = (elapsed_time / total_time) * 100
                logging.debug(
                    f"Function '{func_name}' took {elapsed_time:.6f} seconds [{percentage:.2f}% of total]."
                )
        else:
            result = func(*args, **kwargs)

        return result

    return wrapper


atexit.register(PerformanceTracker.finalize)
