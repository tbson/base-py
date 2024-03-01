import asyncio
from functools import wraps
from typing import Callable

from type.general import Args, Kwargs


def async_task(f: Callable) -> Callable[..., None]:
    @wraps(f)
    def wrapped(*args: Args, **kwargs: Kwargs) -> None:
        try:
            loop = asyncio.get_event_loop()
        except Exception:
            loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        if not callable(f):
            raise TypeError("Task must be a callable")
        loop.run_in_executor(None, f, *args, **kwargs)

    return wrapped
