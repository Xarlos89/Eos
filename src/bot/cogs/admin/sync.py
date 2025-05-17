import os
import logging
from discord.ext import commands


logger = logging.getLogger(__name__)


async def is_admin(ctx) -> bool:
    """ Check if the context user has admin permissions"""
    return ctx.message.author.guild_permissions.administrator

async def is_master_guild(ctx) -> bool:
    """ Check if the context user is in the master guild"""
    return ctx.guild.id == int(os.getenv("MASTER_GUILD"))


class CommandSync(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="sync")
    @commands.check(is_master_guild)
    @commands.check(is_admin)
    async def sync(self, ctx):
        synced = await self.bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s).")

    @sync.error
    async def sync_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            logger.warning(f"{ctx.author.name} has attempted to use the {ctx.invoked_with} command, and was not allowed to do so.")
            await ctx.send('For one reason, or another, YOU cannot use this command.')



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CommandSync(bot))
