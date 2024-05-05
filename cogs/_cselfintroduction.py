from discord.ext import commands

# self‐introduction
# CSelfintroduction


class CSelfIntroduction(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


async def setup(bot: commands.Bot):
    await bot.add_cog(CSelfIntroduction(bot))
