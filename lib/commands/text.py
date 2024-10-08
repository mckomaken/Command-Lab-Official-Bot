import asyncio
import json
import re
from typing import TYPE_CHECKING

import aiofiles

if TYPE_CHECKING:
    from lib.commands.util.consumer import Consumer


ARG_FORMAT = re.compile("%(?:(\\d+)\\$)?([A-Za-z%]|$)")
NULL_ARGUMENT = "null"


class TranslatableTextContent:
    def __init__(self, translate: str, *args: str) -> None:
        self.tr = translate
        self.args: list[str] = list(args)

    @staticmethod
    def parse(tr: str, *args: str) -> str:
        li: list[str] = list()
        content = TranslatableTextContent(tr, args)
        content.for_each_parts(lambda e: li.append(e))

        return "".join(li)

    def for_each_parts(self, consumer: "Consumer[str]"):
        tr = self.tr
        try:
            j = 0
            i = 0
            n = 0
            while match := ARG_FORMAT.match(tr):
                j = n
                k = match.start()
                n = match.end()
                string = ""
                if k > j:
                    string = tr[j:k]
                    if chr(37) in string:
                        raise ValueError("Illegal Argument Exception")
                    consumer.accept(string)
                string = match.group(2)
                string2 = tr[k:n]
                if "%" == string and "%%" == string2:
                    consumer.accept("%")
                else:
                    if not string == "s":
                        raise ValueError(f"Unsupported format: '{string2}")
                    string3 = match.group(1)
                    if string3 is not None:
                        m = int(string3)
                    else:
                        i += 1
                    consumer.accept(self.get_arg(m))

            if j < len(tr):
                string4 = tr[j:]
                if chr(37) in string4:
                    raise ValueError("Illegal Argument Exception")
                consumer.accept(string4)

        except Exception:
            pass

    def get_arg(self, index: int) -> str:
        if index >= 0 and len(self.args):
            obj = self.args[index]
            return NULL_ARGUMENT if obj is None else obj
        else:
            raise ValueError("Illegal Argument Exception")

LANGUAGE_DATA: dict[str, str] = dict()

class Text:
    def __init__(self, text: str):
        self.string = text

    @classmethod
    def of(cls, text: str) -> "Text":
        return Text(text)

    def append(self, text: str):
        self.string += text

    @staticmethod
    def translatable(trans: str):
        tr = LANGUAGE_DATA.get(trans, trans)

        return Text(tr)

    @staticmethod
    def stringifiedTranslatable(trans: str, options: tuple[str]):
        tr = LANGUAGE_DATA.get(trans, trans)

        for opt in options:
            tr = re.sub(r"\%([0-9]\$)?s", opt, tr, 1)

        return Text(tr)

    def getString(self):
        return self.string

    def __str__(self) -> str:
        return self.string

async def load_language():
    global LANGUAGE_DATA
    async with aiofiles.open("./.tmp/ja_jp.json", mode="rb") as fp:
        LANGUAGE_DATA = json.loads(await fp.read())

asyncio.run(load_language())