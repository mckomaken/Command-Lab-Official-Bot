class Pair[A, B]():
    def __init__(self, left: A, right: B) -> None:
        self.left = left
        self.right = right

    def getLeft(self) -> A:
        return self.left

    def setLeft(self, left: A):
        self.left = left

    def getRight(self) -> B:
        return self.right

    def setRight(self, right: B):
        self.right = right

    @staticmethod
    def of(left: A, right: B):
        return Pair(left, right)
