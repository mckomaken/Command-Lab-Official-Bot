class Lifecycle:
    @staticmethod
    @property
    def STABLE():
        return Lifecycle("Stable")

    @staticmethod
    @property
    def EXPERIMENTAL():
        return Lifecycle("Stable")

    def __init__(self, description: str) -> None:
        self.description = description

    def __str__(self) -> str:
        return self.description

    class Depracated():
        def __init__(self, since: int) -> None:
            self.since = since

        def getSince(self):
            return self.since

    def add(self, other: "Lifecycle"):
        if self == Lifecycle.EXPERIMENTAL or other == Lifecycle.EXPERIMENTAL:
            return Lifecycle.EXPERIMENTAL

        if isinstance(self, Lifecycle.Depracated):
            if isinstance(other, Lifecycle.Depracated) and other.since < self.since:
                return other

            return self

        if isinstance(other, Lifecycle.Depracated):
            return other

        return Lifecycle.STABLE