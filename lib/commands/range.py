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
        return string[self.start : self.end]

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    @classmethod
    def between(cls, start: int, end: int):
        return cls(start, end)

    @classmethod
    def at(cls, pos: int):
        return cls(pos, pos)

    @staticmethod
    def encompassing(a: "StringRange", b: "StringRange"):
        return StringRange(min(a.getStart(), b.getStart()), max(a.getEnd(), b.getEnd()))
