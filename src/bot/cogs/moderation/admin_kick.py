"""
Admin command for kicking a user.
"""
import logging
from datetime import datetime

import discord
from discord.ext import commands


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

class AdminKick(commands.Cog):
    """
    Command to kick a user. Takes in a name, and a reason.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Kick a user.")
    @commands.has_permissions(kick_members=True)
    # TODO: DATABASE ROLES.
    # @commands.has_role("Staff")
    async def kick_member(self, ctx, target: discord.Member, reason):
        """
        Take in a user mention, and a string reason.
        """
        # Cant kick bots or admins.
        if not target.bot:
            if not target.guild_permissions.administrator:
                # Message the user, informing them of their fate
                # TODO: Guild specific settings like the contact email
                await target.send(
                    f"## You were kicked by {ctx.author.name}.\n"
                    f"**Reason:** {reason}\n"
                    "\nIf you wish to appeal this kick,"
                    " contact PracticalPythonStaff@gmail.com"
                )
                # Then we do the kick
                await target.kick(reason=f"{ctx.author.name} - {reason}")
                logger.info("{%s} kicked {%s}. Reason: {%s}", ctx.author.name, target.name, reason)
                # Then we publicly announce what happened.
                await ctx.channel.send(embed=embed_info(f"**{ctx.author.name}** kicked **{target.name}**" f"\n**Reason:** {reason}"))

            else:
                await ctx.channel.send(embed=embed_info("You can't kick an Admin."))
        else:
            await ctx.channel.send(embed=embed_info("You cant kick a bot."))

    @kick_member.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.channel.send(embed=embed_info(
                f"User was not found, please check the name and use a mention."))


async def setup(bot) -> None:
    """
    required.
    """
    await bot.add_cog(AdminKick(bot))