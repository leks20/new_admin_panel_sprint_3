import time
from typing import Any
from typing import Callable


def backoff(func: Callable[[Any], Any]) -> Callable[[Any], Callable[[Any], Any]]:
    def inner(
        *args: Any,
        sleep_time: float = 0.1,
        factor: int = 2,
        border_sleep_time: int = 10,
        **kwargs: Any,
    ) -> Callable[[Any], Any]:

        while True:
            try:
                return func(*args, **kwargs)
            except Exception:
                if (sleep_time := sleep_time * (2**factor)) >= border_sleep_time:
                    sleep_time = border_sleep_time

                time.sleep(sleep_time)

    return inner
