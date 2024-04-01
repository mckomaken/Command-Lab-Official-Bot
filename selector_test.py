import os
from lib.commands.exceptions import CommandSyntaxException
from lib.commands.selector import EntitySelectorReader
from brigadier import StringReader
from brigadier.exceptions import CommandSyntaxException as CSE
import asyncio
import readchar
from brigadier.suggestion import SuggestionsBuilder
import colorama

colorama.init()
colorama.just_fix_windows_console()


async def main():
    data = ""
    while True:
        d = readchar.readchar()
        if ord(d) == 0x0008:
            data = data[0:len(data) - 1]
        elif ord(d) == 0x000A or ord(d) == 0x000D:
            data = ""
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
            if data.endswith(","):
                builder = SuggestionsBuilder(data, len(data))
                opts = await reader.suggest_option(builder, None)
            else:
                builder = SuggestionsBuilder(data, data.find("[") + 1)
                opts = await reader.suggest_option_or_end(builder, None)

        elif data == "" or data == "@":
            builder = SuggestionsBuilder(data, 0)
            opts = await reader.suggest_selector(builder, None)
        elif not data.endswith("]"):
            builder = SuggestionsBuilder(data, len(data) - 1)
            opts = await reader.suggest_open(builder, None)

        try:
            reader.read_at_variable()
        except Exception as e:
            if isinstance(e, (CommandSyntaxException, CSE)):
                print(colorama.Fore.RED + e.get_message() + colorama.Fore.RESET)
            else:
                print(colorama.Fore.RED + str(e) + colorama.Fore.RESET)
        else:
            print(f"{colorama.Fore.GREEN}エラーなし{colorama.Fore.RESET}")

        for a in opts.get_list():
            print(f"{colorama.Fore.LIGHTBLACK_EX}{' ' * len(data)}{a.text}{' ' * (30 - len(a.text))}{a.tooltip}{colorama.Fore.RESET}")


if __name__ == "__main__":
    asyncio.run(main())
