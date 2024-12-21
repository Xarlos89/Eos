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

    @commands.command(description="Ban a user.")
    @commands.has_permissions(ban_members=True)
    # TODO: DATABASE ROLES.
    # @commands.has_role("Staff")
    async def ban_member(self, ctx, target: discord.Member, reason):
        """
        Take in a user mention, and a string reason.
        """
        # Cant ban bots or admins.
        if not target.bot:
            if not target.guild_permissions.administrator:
                # Message the user, informing them of their fate
                # TODO: Guild specific settings like the contact email
                await target.send(
                    f"## You were banned by {ctx.author.name}.\n"
                    f"**Reason:** {reason}\n"
                    "\nIf you wish to appeal this ban,"
                    " contact PracticalPythonStaff@gmail.com"
                )
                # Then we do the ban
                await target.ban(reason=f"{ctx.author.name} - {reason}")
                logger.info("{%s} banned {%s}. Reason: {%s}", ctx.author.name, target.name, reason)
                # Then we publicly announce what happened.
                await ctx.channel.send(embed=embed_info(f"**{ctx.author.name}** banned **{target.name}**" f"\n**Reason:** {reason}"))
            else:
                await ctx.channel.send(embed=embed_info("You can't ban an Admin."))
        else:
            await ctx.channel.send(embed=embed_info("You cant ban a bot."))

    @ban_member.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.channel.send(embed=embed_info(
                f"User was not found, please check the name and use a mention."))


async def setup(bot) -> None:
    """
    required.
    """
    await bot.add_cog(AdminBan(bot))