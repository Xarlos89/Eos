"""
Admin command for kicking a user.
"""
import logging
from datetime import datetime, timedelta

import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


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

    @commands.command(description="Time is in minutes to mute a user.")
    @commands.has_permissions(moderate_members=True)
    # TODO: DATABASE ROLES.
    # @commands.has_role("Staff")
    async def mute_member(self, ctx, target: discord.Member, time, reason):
        """
        Take in a user mention, and a string reason.
        """
        # Cant ban bots or admins.
        if not target.bot:
            if not target.guild_permissions.administrator:
                # Message the user, informing them of their fate
                await target.send(f"## You were muted by {ctx.author.name}.\n" f"**Time:** {time} minutes")
                # Then we do the mute
                time_in_mins = datetime.utcnow() + timedelta(minutes=int(time))
                await target.timeout(time_in_mins, reason=None)
                logger.info("{%s} muted {%s} for {%s} minutes. Reason: {%s}", ctx.author.name, target.name, time, reason)
                # Then we publicly announce what happened.
                await ctx.channel.send(
                    embed=embed_info(f"**{ctx.author.name}** muted **{target.name}** for {time} minutes" f"\n**Reason:** {reason}")
                )

            else:
                await ctx.channel.send(embed=embed_info("You can't mute an Admin."))
        else:
            await ctx.channel.send(embed=embed_info("You cant mute a bot."))

    @mute_member.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.channel.send(embed=embed_info(
                f"User was not found, please check the name and use a mention."))


async def setup(bot) -> None:
    """
    required.
    """
    await bot.add_cog(AdminMute(bot))