import logging

from discord.ext import commands

logger = logging.getLogger(__name__)


class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def russian_roulette(self, ctx): ...


async def setup(bot):
    await bot.add_cog(Gambling(bot))
