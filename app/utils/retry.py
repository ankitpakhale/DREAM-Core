import time
from typing import Callable
from app.utils import logger


def retry(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    decorator for retrying a function call with exponential backoff.
    :param max_retries: Maximum number of retries.
    :param delay: Initial delay in seconds.
    :param backoff: Backoff multiplier.
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            """
            Implements retries, logs execution context and reattempts function
            execution on exceptions.
            """
            retries = 0
            current_delay = delay
            while True:
                try:
                    logger.debug(
                        "Executing %s with args: %s kwargs: %s",
                        func.__name__,
                        args,
                        kwargs,
                    )
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    logger.error(
                        "Error in %s: %s (retry %d/%d)",
                        func.__name__,
                        e,
                        retries,
                        max_retries,
                    )
                    if retries >= max_retries:
                        raise
                    time.sleep(current_delay)
                    current_delay *= backoff

        return wrapper

    return decorator
