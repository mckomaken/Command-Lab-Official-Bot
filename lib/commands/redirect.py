from typing import Any, Generic, TypeVar

from lib.commands.context import CommandContext

class RedirectModifier[S]():
    def apply(context: CommandContext[S]) -> list[S]:
        raise NotImplementedError()
