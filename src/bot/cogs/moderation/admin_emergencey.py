import logging
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger(__name__)


def embed_info(message):
    """
    Embedding for things you cant do.
    """
    embed = discord.Embed(
        title=''
        , description=message
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )
    return embed


async def is_administrator(ctx) -> bool:
    """
    Check if the context user has moderator permissions
    https://discordpy.readthedocs.io/en/stable/api.html?highlight=guild_permissions#discord.Permissions.administrator
    """
    return ctx.message.author.guild_permissions.administrator


class AdminEmergencey(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.check(is_administrator)
    @app_commands.command(name="locks down the server.")
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx):
        logger.warning(f"{ctx.guild.name} is going into lockdown mode!")
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(ctx.guild.default_role,send_messages=False)
            await channel.send(f"***{channel.name} is now in lockdown.***")

    @commands.check(is_administrator)
    @app_commands.command(name="unlocks the server after a lockdown")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        logger.warning(f"{ctx.guild.name} is coming out of lockdown mode!")
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(ctx.guild.default_role, send_messages=None)
            await channel.send(f"***{channel.name} has been unlocked.***")

    @lockdown.error
    async def lockdown_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.channel.send(embed=embed_info(
                f"{ctx.author.mention}, you dont have permission to lock down the server. The staff has been notified."))
    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.channel.send(embed=embed_info(
                f"{ctx.author.mention}, you dont have permission to unlock the server. The staff has been notified."))

async def setup(bot) -> None:
    """
    required.
    """
    await bot.add_cog(AdminEmergencey(bot))