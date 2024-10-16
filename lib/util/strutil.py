class StringBuilder:
    _internal: list[str]

    def __init__(self) -> None:
        self._internal = []

    def append(self, string: str):
        self._internal.append(string)
        return self

    def __str__(self) -> str:
        return "".join(self._internal)
