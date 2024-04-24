from discord.ext import commands
import discord
from discord import app_commands
from config.config import config


class crollComButton(discord.ui.View):  # コマンダーランク
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="駆け出し", style=discord.ButtonStyle.gray, emoji="🇦")
    async def pressedCom1(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(965084663855063040)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"{role.mention} を解除しました", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role.mention} を付与しました", ephemeral=True)

    @discord.ui.button(label="初級", style=discord.ButtonStyle.blurple, emoji="🇧")
    async def pressedCom2(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(738936069428478013)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"{role.mention} を解除しました", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role.mention} を付与しました", ephemeral=True)

    @discord.ui.button(label="中級", style=discord.ButtonStyle.red, emoji="🇨")
    async def pressedCom3(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(965084054204608582)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"{role.mention} を解除しました", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role.mention} を付与しました", ephemeral=True)

    @discord.ui.button(label="上級", style=discord.ButtonStyle.green, emoji="🇩")
    async def pressedCom4(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(965084145644601344)  # roll 4
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"{role.mention} を解除しました", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role.mention} を付与しました", ephemeral=True)


class crollJebeButton(discord.ui.View):  # JE or BE & 遊んでる機種
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="JE勢", style=discord.ButtonStyle.green, emoji="<:JE:892256704123772931>", row=0)
    async def pressedJebe1(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(744471714574106664)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"{role.mention} を解除しました", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role.mention} を付与しました", ephemeral=True)

    @discord.ui.button(label="BE勢", style=discord.ButtonStyle.blurple, emoji="<:BE:892256680509861929>", row=0)
    async def pressedJebe2(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(744471657061548223)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"{role.mention} を解除しました", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role.mention} を付与しました", ephemeral=True)

    @discord.ui.button(label="PC", style=discord.ButtonStyle.gray, emoji="🖥️", row=1)
    async def pressedJebe3(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(1103559576953045042)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"{role.mention} を解除しました", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role.mention} を付与しました", ephemeral=True)

    @discord.ui.button(label="スマホ", style=discord.ButtonStyle.gray, emoji="📱", row=1)
    async def pressedJebe4(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(1103559803827146823)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"{role.mention} を解除しました", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role.mention} を付与しました", ephemeral=True)

    @discord.ui.button(label="家庭用ゲーム機", style=discord.ButtonStyle.gray, emoji="🎮", row=1)
    async def pressedJebe5(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(1103559906872795178)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"{role.mention} を解除しました", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role.mention} を付与しました", ephemeral=True)


class crollSenButton(discord.ui.View):  # 宣伝関連 & 質問メンション
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="宣伝し隊", style=discord.ButtonStyle.green, emoji="📝", row=0)
    async def pressedSen1(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(808617738180231178)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"{role.mention} を解除しました", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role.mention} を付与しました", ephemeral=True)

    @discord.ui.button(label="宣伝ウェルカム", style=discord.ButtonStyle.blurple, emoji="📩", row=0)
    async def pressedSen2(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(808618017247330324)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"{role.mention} を解除しました", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role.mention} を付与しました", ephemeral=True)

    @discord.ui.button(label="DM質問OK", style=discord.ButtonStyle.red, emoji="📮", row=0)
    async def pressedSen5(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(972312252889837598)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"{role.mention} を解除しました", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role.mention} を付与しました", ephemeral=True)

    @discord.ui.button(label="JE-質問メンション可", style=discord.ButtonStyle.gray, emoji="<:JE:892256704123772931>", row=1)
    async def pressedSen3(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(888048122616500224)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"{role.mention} を解除しました", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role.mention} を付与しました", ephemeral=True)

    @discord.ui.button(label="BE-質問メンション可", style=discord.ButtonStyle.gray, emoji="<:BE:892256680509861929>", row=1)
    async def pressedSen4(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(888048127699996712)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"{role.mention} を解除しました", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role.mention} を付与しました", ephemeral=True)


class crollHokaButton(discord.ui.View):  # その他
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="通知ON", style=discord.ButtonStyle.gray, emoji="🔔")
    async def pressedHoka1(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(763342542719811605)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"{role.mention} を解除しました", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role.mention} を付与しました", ephemeral=True)

    @discord.ui.button(label="MEE6レベル無効化", style=discord.ButtonStyle.gray, emoji="🔏")
    async def pressedHoka2(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(891286619783581706)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"{role.mention} を解除しました", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role.mention} を付与しました", ephemeral=True)

    @discord.ui.button(label="FOREVER_18", style=discord.ButtonStyle.gray, emoji="🔞")
    async def pressedHoka3(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(892062948531523665)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"{role.mention} を解除しました", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role.mention} を付与しました", ephemeral=True)

    @discord.ui.button(label="bump非表示", style=discord.ButtonStyle.gray, emoji="⤴️")
    async def pressedHoka5(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(873890138063794236)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"{role.mention} を解除しました", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role.mention} を付与しました", ephemeral=True)


class CRoll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="crole", description="【運営】ロール付与するボタンを表示させるコマンドです)")
    @app_commands.checks.has_role(config.administrater_role_id)
    async def croll(self, interaction: discord.Interaction):
        role_embed = discord.Embed(
            title="ロール設定",
            description="該当するロールのボタンを押すと付与されます\nもう一度押すと、解除されます",
            color=0x3aff11
        )
        com_embed = discord.Embed(
            title="コマンダーランク設定",
            description="ーーーーーーーーーー",
            color=0x3aff11
        )
        com_embed.add_field(name="--【@駆け出しコマンダー】--", value="🇦:興味を持っている/これから勉強を始める方はこちら!", inline=False)
        com_embed.add_field(name="--【@初級コマンダー】--", value="🇧:少しでもコマンドができる人はこちら!\n(tp,gamemode,weather,etc.)", inline=False)
        com_embed.add_field(name="--【@中級コマンダー】--", value="🇨:まぁまぁできるかなという方やある程度のアイテムを作れるなどという方はこちら!\n(scoreboard,execute,etc.)", inline=False)
        com_embed.add_field(name="--【@上級コマンダー】--", value="🇩:オリジナルエンティティ・配布MAP・ほぼすべてのコマンドを理解してる人はこちら!\n(execute(複雑),function,etc.)", inline=False)

        jebe_embed = discord.Embed(
            title="JE/BE・機種設定",
            description="ーーーーーーーーーー",
            color=0x3aff11
        )
        jebe_embed.add_field(name="--【@JE(Java)勢】--", value="<:JE:892256704123772931>:Java Editionをプレイしてる人はこちら!", inline=False)
        jebe_embed.add_field(name="--【@BE(統合)勢】--", value="<:BE:892256680509861929>:Bedrock Editionをプレイしてる人はこちら!", inline=False)
        jebe_embed.add_field(name="--【@PC】--", value="🖥️:パソコンを使ってプレイしてる人はこちら !", inline=False)
        jebe_embed.add_field(name="--【@スマホ】--", value="📱:スマートフォンを使ってプレイしてる人はこちら!", inline=False)
        jebe_embed.add_field(name="--【@家庭用ゲーム機】--", value="🎮:家庭用ゲーム機(Switch,PS4,PS5,etc.)を使ってプレイしてる人はこちら!", inline=False)

        sen_embed = discord.Embed(
            title="宣伝・質問受付設定",
            description="ーーーーーーーーーー",
            color=0x3aff11
        )
        sen_embed.add_field(name="--【@宣伝し隊】--", value="📝:宣伝したい人はこのロールを付けて宣伝してください!", inline=False)
        sen_embed.add_field(name="--【@宣伝ウェルカム】--", value="📩:宣伝はしないけど宣伝チャンネルを見たい人はこちら!", inline=False)
        sen_embed.add_field(name="--【@DM質問OK】--", value="📮:DMでの質問対応をしてもいいよという方はこちら!", inline=False)
        sen_embed.add_field(name="--【@java 質問受け付け-メンション可】--", value="<:JE:892256704123772931>:Java Edition に関する質問に回答できる方はこちら!", inline=False)
        sen_embed.add_field(name="--【@be 質問受け付け-メンション可】--", value="<:BE:892256680509861929>:Bedrock Edition に関する質問に回答できる方はこちら!", inline=False)

        hoka_embed = discord.Embed(
            title="その他設定",
            description="ーーーーーーーーーー",
            color=0x3aff11
        )
        hoka_embed.add_field(name="--【@通知ON】--", value="🔔:ゲームの勧誘などの通知が行っても大丈夫な方はこちら!", inline=False)
        hoka_embed.add_field(name="--【@MEE6レベル無効化】--", value="🔏:MEEE6による、レベリング機能がいらないと思った方はこちら!", inline=False)
        hoka_embed.add_field(name="--【@FOREVER_18】--", value="🔞:18禁チャンネル(という名の飯テロチャンネル)を見たい方はこちら !", inline=False)
        hoka_embed.add_field(name="--【@bump非表示】--", value="⤴️:DisboardによるBUMP通知が邪魔だと思った方はこちら!\n(このロールがつくと、<#965098244193542154>が見れなくなります)", inline=False)

        await interaction.response.send_message("実行されました", ephemeral=True)
        await interaction.channel.send(embed=role_embed)
        await interaction.channel.send(embed=com_embed)
        await interaction.channel.send(view=crollComButton())
        await interaction.channel.send(embed=jebe_embed)
        await interaction.channel.send(view=crollJebeButton())
        await interaction.channel.send(embed=sen_embed)
        await interaction.channel.send(view=crollSenButton())
        await interaction.channel.send(embed=hoka_embed)
        await interaction.channel.send(view=crollHokaButton())


async def setup(bot: commands.Bot):
    await bot.add_cog(CRoll(bot))
