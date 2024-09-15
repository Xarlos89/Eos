import logging
import discord
from discord.ext import commands

from core.embeds import embed_info, embed_hc

logger = logging.getLogger(__name__)


class Points(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command()
    async def sync_users(self, ctx: commands.Context) -> None:
        pass

    @commands.hybrid_command()
    async def get_points(self, ctx: commands.Context, user: discord.Member) -> None:

        #TODO: Ended here with some weird JSON decode error: >get_points @xarlos

        points = self.bot.api.get_points(user.id)
        await ctx.reply(points)

    @commands.hybrid_command()
    async def add_points(self, ctx: commands.Context, user: discord.User) -> None:
        pass

    @commands.hybrid_command()
    async def remove_points(self, ctx: commands.Context, user: discord.User) -> None:
        pass




async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Points(bot))
