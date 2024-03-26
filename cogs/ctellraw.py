from discord import ButtonStyle, Embed, SelectOption, TextStyle, app_commands, Interaction
from discord.ui import View, select, Select, button, Button, Modal, TextInput

from discord.ext import commands
from pydantic import BaseModel

from util import create_codeblock


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


class SectionDataText(BaseModel):
    color: str = "reset"
    text: str = ""
    bold: bool = False
    italic: bool = False
    underline: bool = False
    obfuscated: bool = False
    strikethrough: bool = False


def to_command(data: list[SectionDataText]) -> str:
    result: list[str] = []
    for e in data:
        result.append(e.model_dump_json(exclude_defaults=True))

    return f"/tellraw @a [{','.join(result)}]"


def create_tellraw_embed(datas: list[SectionDataText], section: tuple[int]) -> Embed:
    data = datas[section[0]]
    cmd = to_command(datas)

    title = data.text
    if data.bold:
        title = f"**{title}**"
    if data.italic:
        title = f"*{title}*"
    if data.strikethrough:
        title = f"~~{title}~~"
    if data.underline:
        title = f"__{title}__"

    c = get_color(data.color)
    embed = Embed(color=c, title=title)
    embed.add_field(name="出力", value=create_codeblock(cmd))
    embed.set_footer(text=f"Section {section[0] + 1}/{section[1]}")

    return embed


class TellrawModal(Modal):
    def __init__(self, data: list[SectionDataText], section: int, view: View) -> None:
        super().__init__(title="内容を設定", timeout=None)
        self.data = data
        self.section = section
        self.text = TextInput(
            label="名前",
            placeholder="名前がありません",
            style=TextStyle.long,
            default=data[section].text,
            required=False
        )
        self.view = view

        self.add_item(self.text)

    async def on_submit(self, interaction: Interaction):
        self.data[self.section].text = self.text.value or ""
        await interaction.response.edit_message(
            embed=create_tellraw_embed(datas=self.data, section=(
                self.section, len(self.data)
            )),
            view=self.view
        )


class TellrawSection(View):
    def __init__(self, index: int, length: int):
        super().__init__(timeout=None)
        self.section = index
        self.data: list[SectionDataText] = []
        self.length = 0

    @button(label="-", style=ButtonStyle.danger, disabled=True)
    async def remove_section(self, interaction: Interaction, item: Button):
        self.data.pop(self.section)
        self.section = len(self.data) - 1
        if self.section <= 0:
            self.remove_section.disabled = True

        await interaction.response.edit_message(
            embed=create_tellraw_embed(datas=self.data, section=(
                self.section, len(self.data)
            )),
            view=self
        )

    @button(label="<", style=ButtonStyle.secondary, disabled=True)
    async def prev_section(self, interaction: Interaction, item: Button):
        self.section -= 1
        if self.section <= 0:
            self.prev_section.disabled = True
        if self.section < len(self.data) - 1:
            self.next_section.disabled = False

        await interaction.response.edit_message(
            embed=create_tellraw_embed(datas=self.data, section=(
                self.section, len(self.data)
            )),
            view=self
        )

    @button(label="Edit", style=ButtonStyle.primary, disabled=True)
    async def edit_section(self, interaction: Interaction, item: Button):
        await interaction.response.send_modal(TellrawModal(
            self.data, self.section, self
        ))

    @button(label=">", style=ButtonStyle.secondary, disabled=True)
    async def next_section(self, interaction: Interaction, item: Button):
        self.section += 1
        if self.section > 0:
            self.prev_section.disabled = False
        if self.section >= len(self.data) - 1:
            self.next_section.disabled = True

        self.prev_section.disabled = False
        await interaction.response.edit_message(
            embed=create_tellraw_embed(datas=self.data, section=(
                self.section, len(self.data)
            )),
            view=self
        )

    @button(label="+", style=ButtonStyle.success)
    async def add_section(self, interaction: Interaction, item: Button):
        self.data.append(SectionDataText(text="", color="white"))
        self.section = len(self.data) - 1
        self.edit_section.disabled = False
        self.set_color.disabled = False
        self.set_style.disabled = False
        if len(self.data) >= 2:
            self.remove_section.disabled = False
            self.prev_section.disabled = False
        await interaction.response.send_modal(TellrawModal(
            self.data, self.section, self
        ))

    @select(
        placeholder="色",
        options=[SelectOption(label=c, value=c) for c in COLORS],
        disabled=True
    )
    async def set_color(self, interaction: Interaction, item: Select):
        self.data[self.section].color = item.values[0]
        await interaction.response.edit_message(
            embed=create_tellraw_embed(datas=self.data, section=(
                self.section, len(self.data)
            )),
            view=self
        )

    @select(
        placeholder="装飾",
        options=[
            SelectOption(label="太字", value="bold"),
            SelectOption(label="斜体", value="italic"),
            SelectOption(label="下線", value="underline"),
            SelectOption(label="取消線", value="strikethrough"),
            SelectOption(label="隠し", value="obfuscated")
        ],
        disabled=True,
        max_values=5,
        min_values=0
    )
    async def set_style(self, interaction: Interaction, item: Select):
        for i in item.values:
            if i == "bold":
                self.data[self.section].bold = not self.data[self.section].bold
            if i == "italic":
                self.data[self.section].italic = not self.data[self.section].italic
            if i == "underline":
                self.data[self.section].underline = not self.data[self.section].underline
            if i == "obfuscated":
                self.data[self.section].obfuscated = not self.data[self.section].obfuscated
            if i == "strikethrough":
                self.data[self.section].strikethrough = not self.data[self.section].strikethrough

        await interaction.response.edit_message(
            embed=create_tellraw_embed(datas=self.data, section=(
                self.section, len(self.data)
            )),
            view=self
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
