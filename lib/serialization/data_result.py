from plum import dispatch

from lib.commands.util.consumer import Consumer
from lib.commands.util.supplier import Supplier
from lib.serialization.lifecycle import Lifecycle
from lib.util.function import Function
from lib.util.optional import Optional


class K1():
    pass

class App[F, A]():
    pass

class DataResult[R]():
    class Mu(K1):
        pass

    @staticmethod
    def unbox[R](box: App[Mu, R]) -> DataResult[R]:
        return box

    @staticmethod
    @dispatch
    def success[R](result: R) -> DataResult[R]:
        return DataResult.success(result, Lifecycle.EXPERIMENTAL)

    @staticmethod
    @dispatch
    def error[R](message: Supplier[str], partialResult: R) -> DataResult[R]:
        return

    @staticmethod
    @dispatch
    def error[R](message: Supplier[str]) -> DataResult[R]:
        return

    @staticmethod
    @dispatch
    def success[R](result: R, lifecycle: Lifecycle) -> DataResult[R]:
        return DataResult.Success(result, lifecycle)

    @staticmethod
    @dispatch
    def error[R](message: Supplier[str], partialResult: R, lifecycle: Lifecycle) -> DataResult[R]:
        return

    # ---

    def result(self) -> Optional[R]:
        raise NotImplementedError()

    def error(self) -> Optional[DataResult.Error[R]]:
        raise NotImplementedError()

    def getLifecycle(self) -> Lifecycle:
        raise NotImplementedError()

    def hasResultOrPartial(self) -> bool:
        raise NotImplementedError()

    @dispatch
    def resultOrPartial(self, onError: Consumer[str]) -> Optional[R]:
        raise NotImplementedError()

    @dispatch
    def resultOrPartial(self) -> Optional[R]:
        raise NotImplementedError()

    @dispatch
    def getOrThrow[E](self, exceptionSupplier: Function[str, E]):
        raise NotImplementedError()

    @dispatch
    def getPartialOrThrow[E](self, exceptionSupplier: Function[str, E]):
        raise NotImplementedError()

    @dispatch
    def getOrThrow(self) -> R:
        self.getOrThrow(ValueError)

    @dispatch
    def getPartialOrThrow(self):
        self.getPartialOrThrow(ValueError)

    def map[T](self, function: Function[R, T]) -> DataResult[T]:
        raise NotImplementedError()

    def mapOrElse[T](self, successFunction: Function[R, T], errorFunction: Function[DataResult.Error[R], T]) -> T:
        raise NotImplementedError()

    def isSuccess(self) -> bool:
        raise NotImplementedError()

    def isError(self) -> bool:
        return not self.isSuccess()

    def setLifecycle(self, lifecycle: Lifecycle) -> DataResult[R]:
        raise NotImplementedError()


    class Success[R](DataResult[R]):
        def __init__(self, value: R, lifecycle: Lifecycle) -> None:
            self.value = value
            self.lifecycle = lifecycle

        def result(self) -> Optional[R]:
            return Optional.of(self.value)

        def error(self) -> Optional:
            return Optional.empty()

        def hasResultOrPartial(self) -> bool:
            return True

        @dispatch
        def resultOrPartial(self, onError: Consumer[str]) -> Optional[R]:
            return Optional.of(self.value)

        @dispatch
        def resultOrPartial(self):
            return Optional.of(self.value)

        def getOrThrow(self) -> R:
            return self.value

        def getPartialOrThrow(self):
            return self.value

