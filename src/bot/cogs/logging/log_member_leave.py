import logging
import discord
from discord.ext import commands
from datetime import datetime


logger = logging.getLogger(__name__)


def embed_leave(some_member) -> discord.Embed:
    """
    Embedding for user leave alerts.

    :param some_member: discord.Member
         - The member that left the guild.
    """
    embed = discord.Embed(
        title=''
        , description=f'{some_member} has left us.'
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )

    return embed


class LogLeaving(commands.Cog):
    """
    Simple listener to on_member_remove
    then checks the audit log for exact details
    """

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member) -> None:
        """
        First we don't log leaves for unapproved people.
        then we grab the guild, and from there read the last entry in the audit log.
        """
        # TODO: [verification!] - Update this to pull form DB!
        # if "Needs Approval" in [role.name for role in member.roles]:
        #     return

        audit_log = [entry async for entry in member.guild.audit_logs(limit=1)][0]

        if str(audit_log.action) != "AuditLogAction.ban" and str(audit_log.action) != "AuditLogAction.kick":
            embed = embed_leave(member)

            logger.info(f"{member.name} has left {member.guild.name}")
            # # TODO: Replace log channel with entry in the DB.
            # logs_channel = await self.bot.fetch_channel(self.bot.server_settings.log_channel["join_log"])
            # await logs_channel.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """
    Necessary for loading the cog into the bot instance.
    """
    await bot.add_cog(LogLeaving(bot))
