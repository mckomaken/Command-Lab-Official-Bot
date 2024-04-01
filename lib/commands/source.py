from typing import Callable, TypeVar

from lib.commands.suggestions import SuggestionsBuilder
from lib.commands.util import Identifier
from lib.commands.util.consumer import Consumer

T = TypeVar("T")


def common_prefix(a: str, b: str):
    if not a:
        return ''
    for i, c in enumerate(a):
        if c != b[i]:
            return a[:i]
    return a


def should_suggest(remaining: str, candinate: str):
    i = 0
    while candinate.startswith(remaining, i):
        i += 1
        i = candinate.find(chr(95), i)
        if i < 0:
            return False

    return True


class CommandSource():
    @classmethod
    def suggest_identifiers(cls, candinates: list[Identifier], builder: SuggestionsBuilder, prefix: str):
        string = builder.remaining.lower()
        cls.for_each_matching(candinates, string, lambda id: id, lambda id: builder.suggest(str(id)))

        return builder.build_async()

    @classmethod
    def for_each_matching(cls, candinates: list[T], remaining: str, identitfier: Callable[[T], Identifier], action: Consumer[T]):
        bl = remaining.find(chr(58)) > -1
        var5 = iter(candinates)

        while True:
            obj = next(var5, None)
            while obj:
                obj = next(obj, None)
                identifier2 = identitfier(obj)
                if bl:
                    string = str(identifier2)
                    if should_suggest(remaining, string):
                        action.accept(obj)

                elif (should_suggest(remaining, identifier2.get_namespace())
                      or identifier2.get_namespace() == "minecraft" and should_suggest(remaining, identifier2.get_path())):
                    action.accept(obj)
