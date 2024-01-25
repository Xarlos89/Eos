import logging
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


class Admin_Users(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command()
    async def get_all_users(self, ctx: commands.Context) -> None:
        logger.debug("get_all_users command used.")
        await ctx.channel.send(self.bot.api.get_all_users())

    @commands.hybrid_command()
    async def get_user(self, ctx: commands.Context, user: discord.Member) -> None:
        logger.debug("get_user command used.")
        await ctx.channel.send(self.bot.api.get_specific_user(user))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin_Users(bot))

