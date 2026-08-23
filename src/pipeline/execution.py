import inspect
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from functools import wraps
from typing import Any

from src.pipeline.timing_tracker import timing_tracker


def get_time() -> float:
    return time.perf_counter()


@contextmanager
def track_execution(caller_name: str) -> Iterator[None]:
    node = timing_tracker.start(caller_name)
    start_time = get_time()

    try:
        yield
    finally:
        timing_tracker.finish(node, get_time() - start_time)


def execution_time(function: Callable[..., Any]) -> Callable[..., Any]:
    if inspect.iscoroutinefunction(function):

        @wraps(function)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            with track_execution(function.__name__):
                return await function(*args, **kwargs)

        return async_wrapper

    @wraps(function)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        with track_execution(function.__name__):
            return function(*args, **kwargs)

    return sync_wrapper
