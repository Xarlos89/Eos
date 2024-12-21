import logging
from discord.ext import commands

logger = logging.getLogger(__name__)


class admin_emergencey(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="lockdown")
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx):
        logger.warning(f"{ctx.guild.name} is going into lockdown mode!")
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(ctx.guild.default_role,send_messages=False)
            await channel.send(f"***{channel.name} is now in lockdown.***")


    @commands.command(name="unlock")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        logger.warning(f"{ctx.guild.name} is coming out of lockdown mode!")
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(ctx.guild.default_role, send_messages=None)
            await channel.send(f"***{channel.name} has been unlocked.***")


async def setup(bot) -> None:
    await bot.add_cog(admin_emergencey(bot))