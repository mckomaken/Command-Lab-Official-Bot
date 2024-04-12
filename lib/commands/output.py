class CommandOutput:
    def sendMessage():
        raise NotImplementedError()

    def shouldReceiveFeedback() -> bool:
        raise NotImplementedError()

    def shouldTrackOutput() -> bool:
        raise NotImplementedError()

    def shouldBroadcastConsoleToOps() -> bool:
        raise NotImplementedError()

    def cannotBeSilenced() -> bool:
        return False

    @staticmethod
    @property
    def DUMMY():
        class DummyCommandOutput(CommandOutput):
            def sendMessage():
                pass

            def shouldReceiveFeedback() -> bool:
                return False

            def shouldTrackOutput() -> bool:
                return False

            def shouldBroadcastConsoleToOps() -> bool:
                return False

            def cannotBeSilenced() -> bool:
                return False

        return DummyCommandOutput()
