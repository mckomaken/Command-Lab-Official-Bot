from typing import Generic, TypeVar

from lib.commands.context import CommandContext

S = TypeVar("S")


class Command(Generic[S]):
    SINGLE_SUCCESS = 1

    def run(context: CommandContext):
        raise NotImplementedError()
