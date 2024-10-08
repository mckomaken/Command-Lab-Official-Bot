from typing import Callable, Optional


class Nullable[T]():
    def __init__(self, func: Callable[..., T]):
        self._func = func

    def __call__(self, *args, **kwargs) -> Optional[T]:
        try:
            ret = self._func(*args, **kwargs)
        except:
            raise

        return ret
