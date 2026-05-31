import asyncio
import random
import time
from typing import Callable, Any


class RetryConfig:
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        jitter: bool = True,
        retryable_status_codes: set[int] = None,
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.jitter = jitter
        self.retryable_status_codes = retryable_status_codes or {429, 500, 502, 503, 504}


async def retry_with_backoff(
    func: Callable,
    config: RetryConfig,
    *args,
    **kwargs,
) -> Any:
    """Execute an async function with exponential backoff retry logic.

    Handles both hard failures (exceptions, bad status codes) and
    soft failures (via an optional validator function in kwargs).
    """
    validator = kwargs.pop("response_validator", None)
    last_exception = None
    for attempt in range(config.max_retries + 1):
        try:
            result = await func(*args, **kwargs)
            # Check for soft failures if a validator is provided
            if validator and not validator(result):
                if attempt < config.max_retries:
                    delay = min(
                        config.base_delay * (2 ** attempt),
                        config.max_delay,
                    )
                    if config.jitter:
                        delay *= (0.5 + random.random())
                    print(f"Soft failure on attempt {attempt + 1}, retrying in {delay:.1f}s")
                    await asyncio.sleep(delay)
                    continue
                raise ValueError(f"Response failed validation after {config.max_retries + 1} attempts")
            return result
        except Exception as e:
            last_exception = e
            if attempt < config.max_retries:
                delay = min(
                    config.base_delay * (2 ** attempt),
                    config.max_delay,
                )
                if config.jitter:
                    delay *= (0.5 + random.random())
                print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.1f}s")
                await asyncio.sleep(delay)
            else:
                raise last_exception
