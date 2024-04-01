class StringRange:
    start: int
    end: int

    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f"StringRange[start={self.start},end={self.end}]"

    def __len__(self) -> int:
        return self.end - self.start

    def is_empty(self) -> bool:
        return self.start == self.end

    def get(self, string: str) -> str:
        return string[self.start:self.end]

    @classmethod
    def between(cls, start: int, end: int):
        return cls(start, end)

    @classmethod
    def at(cls, pos: int):
        cls(pos, pos)
