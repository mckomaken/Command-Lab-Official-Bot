import discord
from discord import app_commands
from discord.ext import commands


class Itemcount_I2S(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(
            title="【数値変換】アイテム数→スタック数等",
            timeout=None,
            custom_id="itos-modal"
        )

        self.item = discord.ui.TextInput(
            label="アイテム数",
            placeholder="数字で入力してください"
        )

        self.add_item(self.item)

    async def on_submit(self, interaction: discord.Interaction) -> None:

        if not self.item.value.isdecimal():
            await interaction.response.send_message("数字で入力してください", ephemeral=True)
            return
        items = int(self.item.value)

        if items <= 64:
            await interaction.response.send_message(f"なぜ変換にかけた？(笑)\n一応、0スタックと{items}アイテムやで", ephemeral=True)
            return
        elif items <= 128:
            if items == 128:
                stack = "2"
                itemnum = "0"
            else:
                stack = "1"
                itemnum = str(items - 64)
            await interaction.response.send_message(f"2スタックぐらい暗算してくれ......w\n一応、{stack}スタックと{itemnum}アイテムやで", ephemeral=True)
        else:
            lc, lcmod = divmod(items, 3456)
            sc, scmod = divmod(lcmod, 1728)
            st, stmod = divmod(scmod, 64)
            await interaction.response.send_message(f"{items}items = {lc}LC+{sc}c+{st}s+{stmod}i\n-# = {lc}ラージチェスト+{sc}チェスト+{st}スタック+{stmod}アイテム\n-# = {lc * 2 + sc}シュルカーボックス+{st}スタック+{stmod}アイテム")


class Itemcount_S2I(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(
            title="【数値変換】スタック数等→アイテム数",
            timeout=None,
            custom_id="stoi-modal"
        )

        self.item = discord.ui.TextInput(
            label="i-アイテム数",
            placeholder="数字で入力してください",
            required=False,
            default="0",
            row=3
        )
        self.stack = discord.ui.TextInput(
            label="st-スタック数",
            placeholder="数字で入力してください",
            required=False,
            default="0",
            row=2
        )
        self.schest = discord.ui.TextInput(
            label="c-スモールチェスト数(シュル箱数)",
            placeholder="数字で入力してください",
            required=False,
            default="0",
            row=1
        )
        self.lchest = discord.ui.TextInput(
            label="lc-ラージチェスト数",
            placeholder="数字で入力してください",
            required=False,
            default="0",
            row=0
        )

        self.add_item(self.item)
        self.add_item(self.stack)
        self.add_item(self.schest)
        self.add_item(self.lchest)

    async def on_submit(self, interaction: discord.Interaction) -> None:

        if not self.item.value.isdecimal() or not self.stack.value.isdecimal() or not self.schest.value.isdecimal() or not self.lchest.value.isdecimal():
            await interaction.response.send_message("数字で入力してください", ephemeral=True)
            return
        items = int(self.item.value)
        stacks = int(self.stack.value)
        schests = int(self.schest.value)
        lchests = int(self.lchest.value)

        sum = items + stacks * 64 + schests * 1728 + lchests * 3456

        if sum <= 64:
            await interaction.response.send_message(f"なぜ変換にかけた？(笑)\n一応、{sum}アイテムやで", ephemeral=True)
            return
        elif sum <= 128:
            await interaction.response.send_message(f"2スタック以内ぐらいは暗算してくれ......w\n一応、{sum}アイテムやで", ephemeral=True)
        else:
            await interaction.response.send_message(f"{lchests}LC+{schests}c+{stacks}s+{items}i = {sum}i")


class CItemcount(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="citemnum-change", description="実行するとアイテム数を変換してくれます")
    @app_commands.describe(choice="選択肢")
    @app_commands.choices(
        choice=[
            app_commands.Choice(value="i2s", name="アイテム数→スタック数等(10000i→2LC+1c+21st+16i)"),
            app_commands.Choice(value="s2i", name="スタック数等→アイテム数(2LC+1c+21st+16i→10000i)")
        ]
    )
    async def itemcount(self, interaction: discord.Interaction, choice: app_commands.Choice[str]):
        if choice.value == "i2s":
            await interaction.response.send_modal(Itemcount_I2S())
        elif choice.value == "s2i":
            await interaction.response.send_modal(Itemcount_S2I())


async def setup(bot: commands.Bot):
    await bot.add_cog(CItemcount(bot))
