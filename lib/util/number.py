from typing import Union


class Number:
    def __init__(self, value: Union[int, float]) -> None:
        self.value = value

    def intValue(self) -> int:
        return int(self.value)

    def floatValue(self) -> float:
        return float(self.value)

    def byteValue(self) -> int:
        return int(self.value)
