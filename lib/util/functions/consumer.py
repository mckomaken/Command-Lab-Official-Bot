from typing import Callable


class Consumer[T]:
    def __init__(self, cb: Callable[[T], None]) -> None:
        self._cb = cb

    def accept(self, v: T):
        self._cb(v)


class BiConsumer[T, T2]:
    def __init__(self, cb: Callable[[T, T2], None]) -> None:
        self._cb = cb

    def accept(self, v: T, v2: T2):
        self._cb(v, v2)


class ReturnValueConsumer:
    @staticmethod
    @property
    def EMPTY():
        class _EMPTY(ReturnValueConsumer):
            def onResult(self, successful: bool, returnValue: int):
                pass

            def __str__(self) -> str:
                return "<empty>"

        return _EMPTY()

    def onResult(self, successful: bool, returnValue: int):
        raise NotImplementedError()

    def onSuccess(self, successful: int):
        self.onResult(True, successful)

    def onFailure(self):
        self.onResult(False, 0)

    @staticmethod
    def chain(a: "ReturnValueConsumer", b: "ReturnValueConsumer"):
        if a == ReturnValueConsumer.EMPTY:
            return b
        else:

            def _chain(successful, returnValue):
                a.onResult(successful, returnValue)
                b.onResult(successful, returnValue)

            return a if b == ReturnValueConsumer.EMPTY else _chain
