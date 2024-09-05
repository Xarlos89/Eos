import logging
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


class Admin_Settings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command()
    async def get_all_settings(self, ctx: commands.Context) -> None:
        logger.debug("get_settings command used.")
        await ctx.channel.send(self.bot.api.get_all_settings())

    @commands.hybrid_command()
    async def get_guild_settings(self, ctx: commands.Context, guild: discord.Guild) -> None:
        logger.debug("get_settings command used.")
        await ctx.channel.send(self.bot.api.get_settings_for_guild(guild.id))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin_Settings(bot))
