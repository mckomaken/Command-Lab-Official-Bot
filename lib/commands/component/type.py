from abc import ABCMeta, abstractmethod


class ComponentType[T](metaclass=ABCMeta):
    @abstractmethod
    def getCodec(self) -> Codec[T]:
        pass