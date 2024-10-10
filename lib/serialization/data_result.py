from typing import Callable

from plum import dispatch

from lib.serialization.lifecycle import Lifecycle
from lib.util.functions.consumer import Consumer
from lib.util.functions.function import Function
from lib.util.functions.supplier import Supplier
from lib.util.optional import Optional


class K1:
    pass


class App[F, A]:
    pass


class DataResult[R]:
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

    @staticmethod
    def appendMessages(first: str, second: str):
        return f"{first}; {second}"

    # ---

    def result(self) -> Optional[R]:
        raise NotImplementedError()

    def error(self) -> Optional["DataResult.Error[R]"]:
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

    def mapOrElse[
        T
    ](self, successFunction: Function[R, T], errorFunction: Function[DataResult.Error[R], T],) -> T:
        raise NotImplementedError()

    def ifSuccess(self, ifSuccess: Consumer[R]) -> DataResult[R]:
        raise NotImplementedError()

    def ifError(self, ifError: Consumer["DataResult.Error[R]"]) -> DataResult[R]:
        raise NotImplementedError()

    def promotePartial(self, onError: Consumer[str]) -> DataResult[R]:
        raise NotImplementedError()

    def flatMap[R2](self, function: Function[R, DataResult[R2]]) -> DataResult[R2]:
        raise NotImplementedError()

    def setPartial(self, partial: R):
        raise NotImplementedError()

    def isSuccess(self) -> bool:
        raise NotImplementedError()

    def isError(self) -> bool:
        return not self.isSuccess()

    def setLifecycle(self, lifecycle: Lifecycle) -> DataResult[R]:
        raise NotImplementedError()

    def addLifecycle(self, lifecycle: Lifecycle):
        return self.setLifecycle(self.getLifecycle().add(lifecycle))

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

        def getLifecycle(self) -> Lifecycle:
            return self.lifecycle

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

        def map[T](self, function: Function[R, T]) -> DataResult[T]:
            return DataResult.Success(function.apply(self.value), self.lifecycle)

        def mapOrElse[
            T
        ](self, successFunction: Function[R, T], errorFunction: Function[DataResult.Error[R], T],) -> T:
            return successFunction.apply(self.value)

        def ifSuccess(self, ifSuccess: Consumer[R]) -> DataResult[R]:
            ifSuccess.accept(self.value)
            return self

        def ifError(self, ifError: Consumer["DataResult.Error[R]"]) -> DataResult[R]:
            return self

        def promotePartial(self, onError: Consumer[str]) -> DataResult[R]:
            return self

        def flatMap[R2](self, function: Function[R, DataResult[R2]]) -> DataResult[R2]:
            return function.apply(self.value).addLifecycle(self.lifecycle)

        def isSuccess(self) -> bool:
            return True

        def setPartial(self, partial: R):
            raise self

        def __str__(self) -> str:
            return f"DataResult.Success[{self.value}]"

    class Error[R](DataResult[R]):
        def __init__(
            self,
            messageSupplier: Supplier[str],
            partialValue: Optional[R],
            lifecycle: Lifecycle,
        ) -> None:
            self.messageSupplier = messageSupplier
            self.partialValue = partialValue
            self.lifecycle = lifecycle

        def message(self):
            return self.messageSupplier.get()

        def result(self) -> Optional[R]:
            return Optional.empty()

        def error(self) -> Optional:
            return Optional.of(self)

        def hasResultOrPartial(self) -> bool:
            return self.partialValue.isPresent()

        @dispatch
        def resultOrPartial(self, onError: Consumer[str]) -> Optional[R]:
            onError.accept(self.messageSupplier.get())
            return self.partialValue

        @dispatch
        def resultOrPartial(self):
            return self.partialValue

        def getOrThrow[E](self, exceptionSupplier: Function[str, E]) -> R:
            raise exceptionSupplier.apply(self.message())

        def getPartialOrThrow[E](self, exceptionSupplier: Function[str, E]):
            raise exceptionSupplier.apply(self.message())

        def map[T](self, function: Callable[[R], T]) -> DataResult.Error[T]:
            if self.partialValue.isEmpty():
                return self
            return DataResult.Error(self.messageSupplier, self.partialValue.map(function), self.lifecycle)

        def mapOrElse[T](self, successFunction: Function[R, T], errorFunction: Function[R, T]) -> T:
            return errorFunction.apply(self)

        def ifSuccess(self, ifSuccess: Consumer[R]) -> DataResult[R]:
            return self

        def ifError(self, ifError: Consumer[DataResult.Error[R]]) -> DataResult[R]:
            ifError.accept(self)
            return self

        def flatMap[R2](self, function: Function[R, DataResult[R2]]) -> DataResult[R2]:
            if self.partialValue.isEmpty():
                return self

            second = function.apply(self.partialValue.get())
            combinedLifecycle = self.lifecycle.add(second.getLifecycle())
            if isinstance(second, DataResult.Success):
                return DataResult.Error(self.messageSupplier, Optional.of(second.value), combinedLifecycle)
            elif isinstance(second, DataResult.Error):
                return DataResult.Error(
                    lambda _: DataResult.appendMessages(self.messageSupplier.get(), second.messageSupplier.get())
                )
            else:
                raise ValueError()

        def isSuccess(self) -> bool:
            return False

        def __str__(self) -> str:
            return f"DataResult.Error['{self.message()}'{self.partialValue.map(lambda v: f": {v}").orElse("")}]"
