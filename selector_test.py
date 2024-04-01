import os
from lib.commands.exceptions import CommandSyntaxException
from lib.commands.selector import EntitySelectorReader
from brigadier import StringReader
import asyncio
import readchar
from brigadier.suggestion import SuggestionsBuilder


async def main():
    data = ""
    while True:
        d = readchar.readchar()
        if ord(d) == 0x0008:
            data = data[0:len(data) - 1]
        else:
            data += d

        os.system("cls")
        print(data)

        if data == "exit":
            print("Exit.")
            return

        r = StringReader(data)
        r.skip()

        reader = EntitySelectorReader(r, True)
        if "[" in data:
            builder = SuggestionsBuilder(data, data.find("[") + 1)
            opts = await reader.suggest_option_or_end(builder, None)
        elif data == "" or data == "@":
            builder = SuggestionsBuilder(data, 0)
            opts = await reader.suggest_selector(builder, None)
        else:
            builder = SuggestionsBuilder(data, len(data) - 1)
            opts = await reader.suggest_open(builder, None)

        try:
            reader.read_at_variable()
        except Exception as e:
            if isinstance(e, (ValueError, TypeError)):
                print(e)
            else:
                print(e.get_message())

        for a in opts.get_list():
            print(f"{' ' * len(data)}{a.text}{' ' * (30 - len(a.text))}{a.tooltip}")


if __name__ == "__main__":
    asyncio.run(main())
