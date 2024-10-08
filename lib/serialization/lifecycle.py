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