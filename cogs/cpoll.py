import discord
from discord import ButtonStyle, Interaction, app_commands
from discord.ext import commands
from discord.ui import Button, View, button, Modal

from config.config import config
from database import User, session, Oregacha, session2, Polls, session3, func

from datetime import datetime

import random, string

async def win(user_ids, amount, interaction: Interaction, odd):
    for i in user_ids:
        userdb = session.query(User).filter_by(userid=i[0]).first()
        userdb.exp += int(amount * odd)
        touser = interaction.guild.get_member(i[0])
        if amount > 0:
            await touser.send(f"おめでとう！　あなたは **{int(amount * odd)} XP** 獲得した。")
        else:
            await touser.send(f"おめでとう！　あなたは **{int(amount * odd)} XP** 獲得した。\n…… **0 XP** でも勝ちは勝ちだ。")
        if userdb.exp >= 10000:
            userdb.level += 1
            userdb.exp -= 10000
            session.commit()
            mee6_channel = await interaction.guild.fetch_channel(config.channels.level_data)
            await mee6_channel.send(f"mcmdlevel,{userdb.userid},{userdb.username},{userdb.level}")
        else:
            session.commit()

class ShowButton(Button):
    def __init__(self, pollid, choices: str, title: str, started: int):
        super().__init__(label="開票・削除", style=ButtonStyle.danger)
        self.cid = pollid
        self.choices = choices.split(",")
        self.title = title
        self.started = started

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.started:
            await interaction.response.send_message(f"**自分の投票のみ開票・削除ができます！**", ephemeral=True)
            return
        polls = dict(session3.query(Polls.chosen, func.count()).filter_by(pollid=self.cid).group_by(Polls.chosen).all())
        total = (session3.query(func.count()).filter(Polls.pollid==self.cid).scalar())
        if not polls:
            await interaction.message.delete()
        else:
            result_embed = discord.Embed(
                title=f"投票終了！　結果は……", color=0x113AFF
            )
            result_embed.add_field(
                name=f"{self.title}", value="", inline=False
            )

            for n, i in enumerate(self.choices):
                if n in polls:
                    bar = int(40 * polls[n] / total)
                    result_embed.add_field(
                        name=f"{i}: {polls[n]}票", value="="*bar, inline=False
                    )
                else:
                    result_embed.add_field(
                        name=f"{i}: 0票", value="x", inline=False
                    )
                
                result_embed.set_footer(text=f"計{total}票")

            await interaction.channel.send(embed=result_embed)
            await interaction.message.delete()

class ShowBetButton(Button):
    def __init__(self, pollid, choices: str, title: str, rule, nn, amount, odds, started: int):
        super().__init__(label="開票・削除", style=ButtonStyle.danger)
        self.cid = pollid
        self.choices = choices.split(",")
        self.title = title
        self.rule = rule
        self.nn = nn
        self.amount = amount
        self.odds = odds
        self.started = started

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.started:
            await interaction.response.send_message(f"**自分の投票のみ開票・削除ができます！**", ephemeral=True)
            return
        polls = dict(session3.query(Polls.chosen, func.count()).filter_by(pollid=self.cid).group_by(Polls.chosen).all())
        total = (session3.query(func.count()).filter(Polls.pollid==self.cid).scalar())
        if not polls:
            await interaction.message.delete()
        else:
            result_embed = discord.Embed(
                title=f"投票終了！　結果は……", color=0x113AFF
            )
            result_embed.add_field(
                name=f"{self.title}", value="", inline=False
            )

            if self.rule == 3: self.nn = random.randint(1, len(self.choices))

            for n, i in enumerate(self.choices):
                if n in polls:
                    bar = int(40 * polls[n] / total)
                    result_embed.add_field(
                        name=f"{i}（{self.odds[n]}倍）: {polls[n]}票", value="="*bar, inline=False
                    )
                    if self.rule == 1 and polls[n] == 1:
                        user_ids = (session3.query(Polls.userid).filter(Polls.pollid == self.cid, Polls.chosen == n).all())
                        await win(user_ids, self.amount, interaction, self.odds[n])
                    elif self.rule == 2 and n == (self.nn-1):
                        user_ids = (session3.query(Polls.userid).filter(Polls.pollid == self.cid, Polls.chosen == n).all())
                        await win(user_ids, self.amount, interaction, self.odds[n])
                    elif self.rule == 3 and n == (self.nn-1):
                        user_ids = (session3.query(Polls.userid).filter(Polls.pollid == self.cid, Polls.chosen == n).all())
                        await win(user_ids, self.amount, interaction, self.odds[n])
                    elif self.rule == 4 and polls[n] == 2:
                        user_ids = (session3.query(Polls.userid).filter(Polls.pollid == self.cid, Polls.chosen == n).all())
                        await win(user_ids, self.amount, interaction, self.odds[n])
                    elif self.rule == 5 and (polls[n]/total*100 <= self.nn):
                        user_ids = (session3.query(Polls.userid).filter(Polls.pollid == self.cid, Polls.chosen == n).all())
                        await win(user_ids, self.amount, interaction, self.odds[n])
                    elif self.rule == 6 and (n == 0 or polls[n]/total*100 > 50):
                        user_ids = (session3.query(Polls.userid).filter(Polls.pollid == self.cid, Polls.chosen == n).all())
                        await win(user_ids, self.amount, interaction, self.odds[n])

                else:
                    result_embed.add_field(
                        name=f"{i}（{self.odds[n]}倍）: 0票", value="x", inline=False
                    )
                
                if self.rule == 1:
                    result_embed.set_author(name=f"一票だけの選択肢を選んだ人の勝ち！")
                elif self.rule == 2 or self.rule == 3:
                    result_embed.set_author(name=f"{self.choices[self.nn-1]} を選んだ人の勝ち！")
                elif self.rule == 4:
                    result_embed.set_author(name=f"二票だけの選択肢を選んだ人の勝ち！")
                elif self.rule == 5:
                    result_embed.set_author(name=f"割合が {self.nn} % 以下の選択肢を選んだ人の勝ち！")
                result_embed.set_footer(text=f"計{total}票・勝者には DM が届きます（{['','一票のみの選択肢が勝ち','特定の選択肢が勝ち','ランダムな選択肢が勝ち','二票のみの選択肢が勝ち',f'割合が {self.nn} % 以下の選択肢が勝ち','一つ目は絶対に勝ち／二つ目が過半数を占めたら全員勝ち'][self.rule]}）")

            await interaction.channel.send(embed=result_embed)
            await interaction.message.delete()

class ChoiceButton(Button):
    def __init__(self, text, pollid, num, choices: str):
        super().__init__(label=text, style=ButtonStyle.secondary)
        self.num = num
        self.cid = pollid
        self.choices = choices.split(",")

    async def callback(self, interaction: discord.Interaction):
        polled = session3.query(Polls).filter_by(pollid=self.cid, userid=interaction.user.id).first()
        if not polled:
            session3.add(Polls(pollid=self.cid, userid=interaction.user.id, username=interaction.user.name, chosen=self.num))
            session3.commit()
            print(f"{interaction.user.name} -> {self.num}")
            await interaction.response.send_message(f"**{self.label}** に投票しました！", ephemeral=True)
        elif polled:
            await interaction.response.send_message(f"あなたはすでに **{self.choices[polled.chosen]}** に投票しています！", ephemeral=True)

class ChoiceBetButton(Button):
    def __init__(self, text, pollid, num, choices: str, amount, odd):
        super().__init__(label=f"{text} （{odd}倍）", style=ButtonStyle.secondary)
        self.num = num
        self.cid = pollid
        self.amount = amount
        self.choices = choices.split(",")
        self.odd = odd

    async def callback(self, interaction: discord.Interaction):
        polled = session3.query(Polls).filter_by(pollid=self.cid, userid=interaction.user.id).first()
        if not polled:
            userdb = session.query(User).filter_by(userid=interaction.user.id).first()
            userdb.exp -= self.amount
            userdb.allremoveexp += self.amount
            if userdb.exp < 0:
                userdb.level -= 1
                userdb.exp += 10000
            session.commit()
            session3.add(Polls(pollid=self.cid, userid=interaction.user.id, username=interaction.user.name, chosen=self.num))
            session3.commit()
            print(f"{interaction.user.name} -> {self.num}")
            if self.amount > 0:
                await interaction.response.send_message(f"**{self.label}** に投票しました！\n確かに **{self.amount} XP** いただきました。", ephemeral=True)
            else:
                await interaction.response.send_message(f"**{self.label}** に投票しました！\n確かに **{self.amount} XP** を……。\n……ないものはいただけませんね。フリーです！", ephemeral=True)
        elif polled:
            await interaction.response.send_message(f"あなたはすでに **{self.choices[polled.chosen]}** に投票しています！", ephemeral=True)

class ChoiceButtons(View):
    def __init__(self, choices = "x", title = "x", sid = -1):
        super().__init__(timeout=None)
        if len(choices.split(",")) <= 15:
            date = datetime.today().strftime("%Y%m%d")
            rand = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
            for n, i in enumerate(choices.split(",")):
                self.add_item(ChoiceButton(i, f"{date}_{rand}", n, choices))
        self.add_item(ShowButton(f"{date}_{rand}", choices, title, sid))

class ChoiceBetButtons(View):
    def __init__(self, choices = "x", title = "x", amount = 100, rule = 1, nn = None, odds = None, sid = -1):
        super().__init__(timeout=None)
        if len(choices.split(",")) <= 15:
            date = datetime.today().strftime("%Y%m%d")
            rand = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
            for n, i in enumerate(choices.split(",")):
                self.add_item(ChoiceBetButton(i, f"{date}_{rand}", n, choices, amount, odds[n]))
        self.add_item(ShowBetButton(f"{date}_{rand}", choices, title, rule, nn, amount, odds, sid))

class CPoll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="cpoll", description="投票を行います")
    @app_commands.describe(title="タイトル", choice="選択肢／選択肢は , ← カンマで区切ってね！／15個まで")
#    @app_commands.Cooldown(1, 60 * 60)
    async def cpoll(self, interaction: Interaction, title: str, choice: str):
        poler_embed = discord.Embed(
            title=f"投票：{title}", color=0x3AFF11
        )
        poler_embed.set_footer(text="投票者: 表示されません\n開票: 任意のタイミング")
      
        if 16 <= len(choice.split(",")):
            await interaction.response.send_message("**引数が正しくないです！**\n選択肢は15個までです。", ephemeral=True)
            return

        await interaction.response.send_message("投票を開始しました", ephemeral=True)
        await interaction.channel.send(embed=poler_embed, view=ChoiceButtons(choice, title, interaction.user.id))

    @app_commands.command(name="cpollbet", description="XPを賭けて投票を行います（行うのにもXPは必要です）。ルールなども設定できます")
    @app_commands.describe(title="タイトル", choice="選択肢／選択肢は , ← カンマで区切ってね！／2個から15個まで", amount="賭ける量（ 0 ～ 1500 ）", rule="1: 一票のみの選択肢を選んだら勝利, 2: 特定の選択肢が勝利, 3: ランダムな選択肢が勝利, 4: 二票のみの選択肢を選んだら勝利, 5: 割合の小さい選択肢を選んだら勝利, 6: 1つ目は絶対に勝ち／2つ目は過半数なら勝ち", n="2, 5 を設定した場合は設定してください（2は番目／5は割合）。それ以外は0にしてください", odds="選択肢ごとのオッズです（通常2倍、最大2.5倍）。 , ← カンマで区切ってね！")
#    @app_commands.Cooldown(1, 60 * 60)
    async def cpollbet(self, interaction: Interaction, title: str, choice: str, amount: int, rule: int, n: int, odds: str = None):
        poler_embed = discord.Embed(
            title=f"投票：{title}", color=0x3AFF11
        )
        if odds == None:
            odds = ["2.0"] * len(choice.split(","))
        if type(odds) == str: odds = odds.split(",")
        poler_embed.set_footer(text=f"投票者: 表示されません\n開票: 任意のタイミング\n投票時に {amount} XP 徴収されます。\n{['','一票のみの選択肢を選んだら勝ち！','特定の選択肢を選んだら勝ち！', 'ランダムな選択肢が勝ち！', '二票のみの選択肢を選んだら勝ち！', f'割合が {n} % 以下の選択肢を選んだら勝ち！', '一つ目は絶対に勝ち。でも二つ目が過半数を占めたら全員勝ち！'][rule]}\n選択肢ごとのオッズ: {'倍, '.join(odds)}倍")
       
        odds = [float(_) for _ in odds]
      
        if len(choice.split(",")) < 2 or 16 <= len(choice.split(",")):
            await interaction.response.send_message("**引数が正しくないです！**\n選択肢は2個から15個までです。", ephemeral=True)
            return
        elif rule == 6 and len(choice.split(",")) != 2:
            await interaction.response.send_message("**引数が正しくないです！**\nrule に「6」を指定した場合、選択肢は2個のみです。", ephemeral=True)
            return
        elif len(odds) != len(choice.split(",")):
            await interaction.response.send_message("**引数が正しくないです！**\n選択肢の数とオッズの指定数が合っていません。", ephemeral=True)
            return
        elif rule <= 0 or 7 <= rule:
            await interaction.response.send_message("**引数が正しくないです！**\nrule は「1」「2」「3」「4」「5」「6」のみです。", ephemeral=True)
            return
        elif rule == 2 and (n <= 0 or len(choice.split(",")) < n):
            await interaction.response.send_message("**引数が正しくないです！**\nrule に「2」を指定した場合、 n に1以上の数を指定してください！", ephemeral=True)
            return
        elif rule == 5 and (n <= 0 or int(100/len(choice.split(","))) < n):
            await interaction.response.send_message("**引数が正しくないです！**\nrule に「5」を指定した場合、 n は1以上かつ選択肢の数に基づくチャンスレベル以下でなければなりません（2択なら50以下、3択なら33以下、……）。", ephemeral=True)
            return
        elif amount > 1500:
            await interaction.response.send_message("**賭けすぎです！**\n最大 1500 XP となっております。ご利用は計画的に……。", ephemeral=True)
            return
        elif amount < 0:
            await interaction.response.send_message("**引数が正しくないです！**\n賭ける量は 0 ～ 1500 を指定してください。", ephemeral=True)
            return

        for odd in odds:
            if odd > 2.5:
                await interaction.response.send_message("**オッズが高いです！**\n最大2.5倍です。", ephemeral=True)
                return
            elif odd < 0:
                await interaction.response.send_message("**引数が正しくないです！**\nオッズは 0 ～ 2.5 を指定してください。", ephemeral=True)
                return

        userdb = session.query(User).filter_by(userid=interaction.user.id).first()
        userdb.exp -= amount * 2
        userdb.allremoveexp += amount * 2
        if userdb.exp < 0:
            userdb.level -= 1
            userdb.exp += 10000
        session.commit()

        if amount > 0:
            await interaction.response.send_message(f"投票を開始しました！\n確かに **{amount * 2} XP** いただきました。", ephemeral=True)
        else:
            await interaction.response.send_message(f"投票を開始しました！\n確かに **{amount * 2} XP** を……。\n……ないものはいただけませんね。フリーでお楽しみください！", ephemeral=True)
        await interaction.channel.send(embed=poler_embed, view=ChoiceBetButtons(choice, title, amount, rule, n, odds, interaction.user.id))

async def setup(bot: commands.Bot):
    await bot.add_cog(CPoll(bot))
