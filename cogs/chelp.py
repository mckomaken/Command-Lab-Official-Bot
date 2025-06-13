import discord
from discord import app_commands
from discord.ext import commands
# import random
import json

COMMANDS = [
    "chelp",
    "chelp-all",
]


class CHelp_com(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="chelp", description="各コマンドの詳細な説明を表示します")
    @app_commands.describe(command="知りたいコマンド名を入力してください")
    async def ctranslate(self, interaction: discord.Interaction, command: str):
        await interaction.response.defer(thinking=True)
        with open("data/json_chelp_command.json", "r", encoding="utf-8") as f:
            jsonfile = json.load(f)
            cmdname = jsonfile[command]
        arglist = []
        description = str(cmdname["description"]).replace("\\n", "\n")
        cmdid = cmdname["cmdid"]
        admintf = "【運営専用】" if cmdname["admin"] is True else ""
        if cmdname["args"] == []:
            args = ""
        else:
            for i in range(len(jsonfile[command]["args"])):
                text = "### " if i % 2 == 0 else ""
                argdesc = f"{text}{jsonfile[command]["args"][i]}"
                arglist.append(argdesc)
                args = f'\n{"\n".join(arglist)}'
        syntax = f"### 【構文】\n{cmdname["syntax"]}" if cmdname["syntax"] != "" else ""
        example = f"### 【例文】\n{cmdname["example"]}" if cmdname["example"] != "" else ""
        EMBEDDESC = f"""
## </{command}:{cmdid}> {admintf}
{description}{args}
{syntax}
{example}
"""
        help_embed = discord.Embed(
            description=EMBEDDESC,
            color=0x60ff99
        )
        await interaction.followup.send(embed=help_embed, silent=True)

    @ctranslate.autocomplete("command")
    async def command_autocomplete(self, interaction: discord.Interaction, current: str):
        filtered_commands = [cmd for cmd in COMMANDS if current.lower() in cmd.lower()]
        return [app_commands.Choice(name=cmd, value=cmd) for cmd in filtered_commands[:25]]


async def setup(bot: commands.Bot):
    await bot.add_cog(CHelp_com(bot))
