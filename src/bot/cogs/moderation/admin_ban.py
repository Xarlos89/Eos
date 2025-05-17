"""
Admin command for kicking a user.
"""
import os
import logging
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from .._checks import is_master_guild, is_moderator

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


class AdminBan(commands.Cog):
    """
    Command to ban a user. Takes in a name, and a reason.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.check(is_moderator)
    @commands.check(is_master_guild)
    @commands.has_permissions(ban_members=True)
    @app_commands.command(description="Ban a user.")
    async def ban_member(self, interaction: discord.Interaction, target: discord.Member, reason: str):
        """
        Take in a user mention, and a string reason.
        """
        # Cant ban bots or admins.
        if not target.bot:
            if not target.guild_permissions.administrator:
                # Message the user, informing them of their fate
                # TODO: Guild specific settings like the contact email
                await interaction.response.defer()
                await target.send(
                    f"## You were banned by {interaction.user.name}.\n"
                    f"**Reason:** {reason}\n"
                    "\nIf you wish to appeal this ban,"
                    " contact PracticalPythonStaff@gmail.com"
                )
                # Then we do the ban
                await target.ban(reason=f"{interaction.user.name} - {reason}")
                logger.info("{%s} banned {%s}. Reason: {%s}", interaction.user.name, target.name, reason)
                # Then we publicly announce what happened.
                await interaction.followup.send(
                    embed=embed_info(f"**{interaction.user.name}** banned **{target.name}**" f"\n**Reason:** {reason}"))
            else:
                await interaction.channel.send(embed=embed_info("You can't ban an Admin."))
        else:
            await interaction.channel.send(embed=embed_info("You cant ban a bot."))

    @ban_member.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.channel.send(embed=embed_info(
                f"User was not found, please check the name and use a mention."))

        if isinstance(error, commands.CheckFailure):
            await ctx.channel.send(embed=embed_info(
                f"{ctx.author.mention}, you dont have permission to ban users. The staff has been notified."))


async def setup(bot) -> None:
    """
    required.
    """
    await bot.add_cog(AdminBan(bot))
