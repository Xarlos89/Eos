"""
Admin command for kicking a user.
"""
import logging
from datetime import datetime

import discord
from discord.ext import commands
from discord import app_commands

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


async def is_moderator(ctx) -> bool:
    """
    Check if the context user has moderator permissions
    https://discordpy.readthedocs.io/en/stable/api.html?highlight=guild_permissions#discord.Permissions.kick_members
    """
    return ctx.message.author.guild_permissions.kick_members


class AdminKick(commands.Cog):
    """
    Command to kick a user. Takes in a name, and a reason.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.check(is_moderator)
    @app_commands.command(description="Kick a user.")
    @commands.has_permissions(kick_members=True)
    async def kick_member(self, interaction: discord.Interaction, target: discord.Member, reason: str):
        """
        Take in a user mention, and a string reason.
        """
        # Cant kick bots or admins.
        if not target.bot:
            await interaction.response.defer()
            if not target.guild_permissions.administrator:
                # Message the user, informing them of their fate
                # TODO: Guild specific settings like the contact email
                await target.send(
                    f"## You were kicked by {interaction.user.name}.\n"
                    f"**Reason:** {reason}\n"
                    "\nIf you wish to appeal this kick,"
                    " contact PracticalPythonStaff@gmail.com"
                )
                # Then we do the kick
                await target.kick(reason=f"{interaction.user.name} - {reason}")
                logger.info("{%s} kicked {%s}. Reason: {%s}", interaction.user.name, target.name, reason)
                # Then we publicly announce what happened.
                await interaction.channel.send(
                    embed=embed_info(f"**{interaction.user.name}** kicked **{target.name}**" f"\n**Reason:** {reason}"))

            else:
                await interaction.channel.send(embed=embed_info("You can't kick an Admin."))
        else:
            await interaction.channel.send(embed=embed_info("You cant kick a bot."))

    @kick_member.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.channel.send(embed=embed_info(
                f"User was not found, please check the name and use a mention."))

        if isinstance(error, commands.CheckFailure):
            await ctx.channel.send(embed=embed_info(
                f"{ctx.author.mention}, you dont have permission to kick users. The staff has been notified."))


async def setup(bot) -> None:
    """
    required.
    """
    await bot.add_cog(AdminKick(bot))
