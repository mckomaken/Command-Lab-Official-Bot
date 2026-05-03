import asyncio
import discord
from discord.ext import commands

from datetime import datetime, timezone


STATUSES = [
    ("JavaEditionをプレイ中", "playing", 120),
    ("BedrockEditionをプレイ中", "playing", 120),
    ("BugEditionをプレイ中(笑)", "playing", 10),
    ("EducationEditionをプレイ中", "playing", 120),
    ("データパックを作成中", "playing", 120),
    ("データパックをデバッグ中", "playing", 120),
    ("NOW: %TIME% (UTC+9)", "time", 20),
    ("マイクラのコマンドを勉強中", "playing", 100),
    ("discord.pyとpythonを勉強中", "playing", 100),
    ("Javaを勉強中", "playing", 100),
    ("JavaScriptを勉強中", "playing", 100),
    ("コマ研Botはいつでもあなたのメッセージを見ている", "watching", 20),
    ("大体何でもできるのだ♪", "watching", 30),
    ("私はボットです", "playing", 30),
    ("Netflixで映画を視聴中", "watching", 30),
    ("NOW: %TIME% (UTC+9)", "time", 20),
    ("ポテトをツンツン中", "playing", 30),
    ("腐ったジャガイモを栽培中", "playing", 30),
    ("YouTubeを視聴中", "watching", 60),
    ("新規機能随時募集中！", "watching", 60),
    ("お買い物中", "playing", 40),
    ("春菊を調理中", "playing", 40),
    ("すき焼きを食事中", "playing", 40),
    ("春菊の配信を視聴中", "watching", 10),
    ("コマ研ができてから%CREATED_AT%経過", "created_at", 30),
    ("ニコニコ動画を視聴中", "watching", 60),
    ("Spotifyを再生中", "listening", 60),
    ("私の誕生日は3月3日です", "playing", 120),
    ("MINCERAFT", "playing", 10),
    ("NOW: %TIME% (UTC+9)", "time", 20),
    ("新規機能随時募集中！", "watching", 60),
    ("サーバー人数%MEMBER_COUNT%人ありがとう!", "member_count", 120),
    ("コマ研%SERVER_ANNIVERSARY%周年ありがとう!", "server_anniversary", 120),
    ("睡眠中(再起動してないよ)", "playing", 60),
    ("エンダードラゴンを討伐中", "playing", 90),
    ("シュルカーのせいで浮遊中", "playing", 30),
    ("水バケツ着地失敗", "playing", 10),
    ("ぽこあポケモンに浮気中", "playing", 60),
    ("マリカワールドに浮気中", "playing", 60),
    ("無事回収してエリトラで飛行中", "playing", 60),
    ("NOW: %TIME% (UTC+9)", "time", 20),
    ("ファンアート募集中！", "playing", 60),
    ("鉱石ガチャのためにブランチマイニング中", "playing", 90),
    ("天空TTでツルハシを修繕中", "playing", 120),
    ("諦めてQuarryで露天掘り中", "playing", 150),
    ("サーバーを管理中", "playing", 60),
    ("キャッシュを整理中", "playing", 60),
    ("誰かコマ研まめ知識作って", "playing", 60),
    ("XPを計算中", "playing", 30),
    ("コマ研ができてから%CREATED_AT%経過", "created_at", 30),
    ("NOW: %TIME% (UTC+9)", "time", 20),
]


class ChangeStatus(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            for name, activity_type, delay in STATUSES:
                if activity_type == "playing":
                    activity = discord.Activity(type=discord.ActivityType.playing, name=name)
                elif activity_type == "watching":
                    activity = discord.Activity(type=discord.ActivityType.watching, name=name)
                elif activity_type == "listening":
                    activity = discord.Activity(type=discord.ActivityType.listening, name=name)
                elif activity_type == "time":
                    activity = discord.Activity(type=discord.ActivityType.playing, name=name.replace("%TIME%", datetime.now().strftime("%Y/%m/%d-%H:%M:%S")))
                elif activity_type == "member_count":
                    activity = discord.Activity(type=discord.ActivityType.playing, name=name.replace("%MEMBER_COUNT%", str(len(self.bot.users))))
                elif activity_type == "created_at":  # サーバー作成日時からの経過時間
                    created_at = self.bot.guilds[0].created_at  # 最初のサーバーの作成日時を取得
                    elapsed_time_tick = str((datetime.now(timezone.utc) - created_at).seconds * 20).split(".")[0]
                    elapsed_time_days = str((datetime.now(timezone.utc) - created_at).days).split(".")[0]
                    activity = discord.Activity(type=discord.ActivityType.playing, name=name.replace("%CREATED_AT%", f"{elapsed_time_tick}tick(≒{elapsed_time_days}日)"))
                elif activity_type == "server_anniversary":  # サーバー周年記念
                    created_at = self.bot.guilds[0].created_at  # 最初のサーバーの作成日時を取得
                    elapsed_time_year = str((datetime.now(timezone.utc) - created_at).days // 365)
                    activity = discord.Activity(type=discord.ActivityType.playing, name=name.replace("%SERVER_ANNIVERSARY%", elapsed_time_year))
                else:
                    continue

                await self.bot.change_presence(activity=activity)
                await asyncio.sleep(delay)



async def setup(bot: commands.Bot):
    await bot.add_cog(ChangeStatus(bot))
