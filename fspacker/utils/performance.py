import atexit
import logging
import time
from functools import wraps
from threading import Lock


class PerformanceTracker:
    """Performance tracker class."""

    global_start_time = None
    function_times = {}
    total_time = 0.0
    lock = Lock()

    @classmethod
    def initialize(cls):
        if cls.global_start_time is None:
            cls.global_start_time = time.perf_counter()
            cls.function_times = {}
            cls.total_time = 0.0

    @classmethod
    def update_total_time(cls):
        if cls.global_start_time is not None:
            cls.total_time = time.perf_counter() - cls.global_start_time

    @classmethod
    def finalize(cls):
        if cls.global_start_time is not None:
            cls.update_total_time()
            logging.debug(
                f"{'-'*20}Summary{'-'*20}\n[*] Total application runtime: {cls.total_time:.6f} seconds."
            )
            for func_name, elapsed_time in cls.function_times.items():
                percentage = (
                    (elapsed_time / cls.total_time) * 100
                    if cls.total_time > 0
                    else 0
                )
                logging.debug(
                    f"Function '{func_name}' total time: {elapsed_time:.6f} seconds ({percentage:.2f}% of total runtime)."
                )
            cls.global_start_time = None


def perf_tracker(func):
    """Decorator function to test performance."""

    PerformanceTracker.initialize()

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        with PerformanceTracker.lock:
            func_name = f"{func.__module__}.{func.__name__}"
            PerformanceTracker.function_times[func_name] = (
                PerformanceTracker.function_times.get(func_name, 0)
                + elapsed_time
            )

        PerformanceTracker.update_total_time()
        total_time = PerformanceTracker.total_time
        if total_time > 0:
            percentage = (elapsed_time / total_time) * 100
            logging.debug(
                f"Function '{func_name}' took {elapsed_time:.6f} seconds ({percentage:.2f}% of total runtime)."
            )

        return result

    return wrapper


atexit.register(PerformanceTracker.finalize)
