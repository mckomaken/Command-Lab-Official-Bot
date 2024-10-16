from __future__ import annotations

from typing import Any

from plum import dispatch


class Array[T]:
    _internal: list[T | None] | None
    _capacity: int | None
    _lazy: bool

    @dispatch
    def __init__(self, capacity: int | None) -> None:
        if capacity is None:
            self._internal = None
            self._capacity = None
            self._lazy = True
        else:
            self._internal = capacity * [None]
            self._capacity = capacity
            self._lazy = False
        self.cursor = 0

    @dispatch
    def __init__(self, initialValue: list[T]):
        self._internal = initialValue
        self._capacity = len(initialValue)
        self._lazy = False
        self.cursor = 0

    def __call__(self, capacity: int | None = None) -> Array[T]:
        for i in range(self.length):
            self._internal[i] = Array[T](capacity)

        return self

    def __iter__(self) -> list[T]:
        return self._internal

    def __len__(self):
        return self.length

    def __getitem__(self, key: int) -> T:
        if not self._internal:
            raise UnboundLocalError()
        if self._capacity is None:
            raise UnboundLocalError()
        if self._capacity <= key:
            raise IndexError()

        return self._internal[key]

    def __setitem__(self, key: int, value: Any) -> None:
        if self._capacity <= key:
            raise IndexError()

        if self._lazy is True and isinstance(value, Array):
            self._capacity = value.length

        self._internal[key] = value

    @property
    def length(self):
        return self._capacity
