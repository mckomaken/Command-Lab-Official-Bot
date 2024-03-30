import json
import aiofiles


class Text():
    def __init__(self, text: str):
        self.string = text

    @classmethod
    def of(cls, text: str) -> "Text":
        return Text(text)

    def append(self, text: str):
        self.string += text

    @classmethod
    async def translatable(cls, trans: str):
        async with aiofiles.open("./tmp/ja_jp.json") as fp:
            data = json.loads(await fp.read())

        return Text(data[trans])

    def get_string(self):
        return self.string
