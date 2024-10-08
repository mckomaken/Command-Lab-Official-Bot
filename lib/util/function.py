from typing import Callable, TypeVar

R = TypeVar("R")
T = TypeVar("T")
T1 = TypeVar("T1")

Function = Callable[[T], R]
BiFunction = Callable[[T, T1], R]