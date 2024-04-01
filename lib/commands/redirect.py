from typing import Generic, TypeVar

from lib.commands.context import CommandContext

S = TypeVar("S")


class RedirectModifier(Generic[S]):
    def apply(context: CommandContext[S]) -> list[S]:
        raise NotImplementedError()
