from typing import Any, Generic, TypeVar

E = TypeVar("E")


class Interner(Generic[E]):
    def __init__(self) -> None:
        self.map: dict[E, Any] = dict()

    def intern(self, sample: E) -> E:
        sneaky = None
        while sneaky is None:
            entry = self.map.get(sample, None)
            if entry is not None:
                if sample is not None:
                    return sample

            sneaky = self.map.setdefault(sample, None)

        return sample
