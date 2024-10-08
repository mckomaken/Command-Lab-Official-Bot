class DynamicOps[T]():
    def empty(self) -> T:
        raise NotImplementedError()
    
    def emptyMap(self) -> T:
        return
    
    def emptyList(self) -> T:
        return
    
    def convertTo[U](self, outOps: "DynamicOps[U]", input: T) -> U:
        raise NotImplementedError()
    
    def 