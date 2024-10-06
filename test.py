from collections.abc import Callable
from typing import Any, Optional

from multipledispatch import dispatch


class prop(property):
    def __init__(self, fget = ..., fset = ..., fdel = ..., doc: str = ...) -> None:
        super().__init__(fget, fset, fdel)

    def __get__(self, i, _):
        val = self.fget(i)
        class _P(type(val)):
            def __call__(_self, val: Any = None):
                if val is None:
                    return _self
                else:
                    return self.fset(i, val)

        return _P(val)

class classprop[T]():
    def __init__(self, type: type[T], initialValue: T):
        self.type = type
        self.value = initialValue

    def __get__(self, instance, owner) -> T | Callable[[Optional[T]], T]:
        class _P(self.type):
            def __call__(_self, val: Any = None):
                if val is None:
                    return _self
                else:
                    self.value = val
        return _P(self.value)

    def __set__(self, instance, val: T):
        self.value = val


class Test():
    prop1 = classprop(int, 2)

a = Test()
print(a.prop1)
a.prop1(20)
print(a.prop1())
