import asyncio
import os

import colorama
import readchar

from lib.commands.dispatcher import CommandDispatcher
from lib.commands.entity import Entity, EntityType
from lib.commands.exceptions import CommandSyntaxException
from lib.commands.output import CommandOutput
from lib.commands.reader import StringReader
from lib.commands.server import MinecraftServer
from lib.commands.source import ServerCommandSource
from lib.commands.util import Vec2f, Vec3d
from lib.commands.world import ServerWorld, World

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

        if data == "":
            return

        r = StringReader(data)

        try:
            dispatcher = CommandDispatcher()
            parsed = dispatcher.parse(r, ServerCommandSource(
                CommandOutput.DUMMY, Vec3d(0, 0, 0), Vec2f(0, 0), ServerWorld(), 1, "akpc_0504", "ap12",
                MinecraftServer(), Entity(EntityType.PLAYER, World()), False, print
            ))
            opts = await dispatcher.getCompletionSuggestions(parsed, None)

        except Exception as e:
            if isinstance(e, CommandSyntaxException):
                print(colorama.Fore.RED + e.get_message() + colorama.Fore.RESET)
            else:
                print(colorama.Fore.RED + str(e) + colorama.Fore.RESET)
        else:
            print(f"{colorama.Fore.GREEN}エラーなし{colorama.Fore.RESET}")

            for a in opts.get_list():
                print(f"{colorama.Fore.LIGHTBLACK_EX}{' ' * len(data)}{a.text}{' ' * (30 - len(a.text))}{a.tooltip}{colorama.Fore.RESET}")


if __name__ == "__main__":
    asyncio.run(main())
