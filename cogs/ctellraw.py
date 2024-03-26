from discord import ButtonStyle, Embed, SelectOption, TextStyle, app_commands, Interaction
from discord.ui import View, select, Select, button, Button, Modal, TextInput

from discord.ext import commands
from pydantic import BaseModel


COLORS: list[str] = [
    "black", "dark_blue", "dark_green", "dark_aqua", "dark_red",
    "dark_purple", "gold", "gray", "dark_gray", "blue", "green",
    "aqua", "red", "light_purple", "yellow", "white"
]


def get_color(color: str) -> int | None:
    if color == "black":
        return 0x000000
    elif color == "dark_blue":
        return 0x0000AA
    elif color == "dark_green":
        return 0x00AA00
    elif color == "dark_aqua":
        return 0x00AAAA
    elif color == "dark_red":
        return 0xAA0000
    elif color == "dark_purple":
        return 0xAA00AA
    elif color == "gold":
        return 0xFFAA00
    elif color == "gray":
        return 0xAAAAAA
    elif color == "dark_gray":
        return 0x555555
    elif color == "blue":
        return 0x5555FF
    elif color == "green":
        return 0x55FF55
    elif color == "aqua":
        return 0x55FFFF
    elif color == "red":
        return 0xFF5555
    elif color == "light_purple":
        return 0xFF55FF
    elif color == "yellow":
        return 0xFFFF55
    elif color == "white":
        return 0xFFFFFF
    else:
        return None


def create_tellraw_embed(color: str, text: str, section: tuple[int]) -> Embed:
    c = get_color(color)
    embed = Embed(color=c, title="Tellraw Editor", description=text)
    embed.set_footer(text=f"Section {section[0]}/{section[1]}")

    return embed


class SectionDataText(BaseModel):
    color: str
    text: str
    bold: bool = False
    italic: bool = False


class TellrawModal(Modal):
    def __init__(self, data: list[SectionDataText], section: int) -> None:
        super().__init__(title="内容を設定", timeout=None)
        self.data = data
        self.section = section
        self.text = TextInput(
            label="名前",
            placeholder="名前がありません",
            style=TextStyle.long
        )

        self.add_item(self.text)

    async def on_submit(self, interaction: Interaction):
        self.data[self.section].text = self.text.value
        await interaction.response.edit_message(
            embed=create_tellraw_embed(color=self.data[self.section].color, text=self.data[self.section].text, section=(
                self.section, len(self.data)
            ))
        )


class TellrawSection(View):
    def __init__(self, index: int, length: int):
        super().__init__(timeout=None)
        self.section = index
        self.data: list[SectionDataText] = []
        self.length = 0

    @button(label="-", style=ButtonStyle.danger, disabled=True)
    async def remove_section(self, interaction: Interaction, item: Button):
        self.section = 0
        await interaction.response.edit_message(
            embed=create_tellraw_embed(color=self.data[self.section].color, text=self.data[self.section].text, section=(
                self.section,
            ))
        )

    @button(label="<", style=ButtonStyle.secondary, disabled=True)
    async def prev_section(self, interaction: Interaction, item: Button):
        self.section -= 0
        await interaction.response.edit_message(
            embed=create_tellraw_embed(color=self.data[self.section].color, text=self.data[self.section].text, section=(
                self.section, len(self.data)
            ))
        )

    @button(label="Edit", style=ButtonStyle.primary)
    async def edit_section(self, interaction: Interaction, item: Button):
        await interaction.response.send_modal(TellrawModal(self.data, self.section))

    @button(label=">", style=ButtonStyle.secondary)
    async def next_section(self, interaction: Interaction, item: Button):
        self.section += 0
        await interaction.response.edit_message(
            embed=create_tellraw_embed(color=self.data[self.section].color, text=self.data[self.section].text, section=(
                self.section, len(self.data)
            ))
        )

    @button(label="+", style=ButtonStyle.success)
    async def add_section(self, interaction: Interaction, item: Button):
        self.data.append(SectionDataText(text="", color="white"))
        self.section = 0
        await interaction.response.edit_message(
            embed=create_tellraw_embed(color=self.data[self.section].color, text=self.data[self.section].text, section=(
                self.section, len(self.data)
            ))
        )

    @select(
        placeholder="色",
        options=[SelectOption(label=c, value=c) for c in COLORS]
    )
    async def set_color(self, interaction: Interaction, item: Select):
        self.color = item.values[0]
        await interaction.response.edit_message(
            embed=create_tellraw_embed(color=self.color, text=self.text, section=(
                self.section,
            ))
        )


class CTellraw(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ctellraw")
    @app_commands.guild_only()
    async def tellraw(self, interaction: Interaction):

        await interaction.response.send_message(view=TellrawSection(0, 1))


async def setup(bot: commands.Bot):
    await bot.add_cog(CTellraw(bot))
