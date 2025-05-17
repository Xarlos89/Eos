"""
Admin command for kicking a user.
"""
import os
import logging
from datetime import datetime, timedelta

import discord
from discord.ext import commands
from discord import app_commands

from .._checks import is_master_guild, is_moderator

logger = logging.getLogger(__name__)


def embed_info(message):
    """
    Embedding for general things
    """
    embed = discord.Embed(
        title=''
        , description=message
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )
    return embed


def embed_info(message):
    """
    Embedding for generl things
    """
    embed = discord.Embed(
        title=''
        , description=message
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )
    return embed


class AdminMute(commands.Cog):
    """
    Command to ban a user. Takes in a name, and a reason.
    """

    def __init__(self, bot):
        self.bot = bot

    @is_moderator()
    @is_master_guild()
    @app_commands.command(description="Time is in minutes to mute a user.")
    @commands.has_permissions(moderate_members=True)
    async def mute_member(self, interaction: discord.Interaction, target: discord.Member, time: str, reason: str):
        """
        Take in a user mention, and a string reason.
        """
        # Cant ban bots or admins.
        if not target.bot:
            logger.info("0")
            if not target.guild_permissions.administrator:
                # Message the user, informing them of their fate
                await interaction.response.defer()
                try:
                    await target.send(f"## You were muted by {interaction.user.name}.\n" f"**Time:** {time} minutes")
                except:
                    logger.info(f"{target.name} was muted, but cannot be sent a DM.")
                # Then we do the mute
                await target.timeout(timedelta(minutes=float(time)), reason=None)
                logger.info("%s muted %s for %s minutes. Reason: %s", interaction.user.name, target.name, time,
                            reason)
                # Then we publicly announce what happened.
                await interaction.followup.send(
                    embed=embed_info(
                        f"**{interaction.user.name}** muted **{target.name}** for {time} minutes" f"\n**Reason:** {reason}")
                )
            else:
                await interaction.channel.send(embed=embed_info("You can't mute an Admin."))
        else:
            await interaction.channel.send(embed=embed_info("You cant mute a bot."))

    @mute_member.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.channel.send(embed=embed_info(
                f"User was not found, please check the name and use a mention."))

        if isinstance(error, commands.CheckFailure):
            await ctx.channel.send(embed=embed_info(
                f"{ctx.author.mention}, you dont have permission to mute users. The staff has been notified."))


async def setup(bot) -> None:
    """
    required.
    """
    await bot.add_cog(AdminMute(bot))
