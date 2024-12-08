"""
Logs when a member leaves.
"""
import logging
from datetime import datetime
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


def embed_leave(some_member):
    """
    Embedding for user leave alerts.
    """
    embed = discord.Embed(
        title=''
        , description=f'{some_member} has left us.'
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )
    return embed


class LoggingLeaves(commands.Cog):
    """
    Simple listener to on_member_update
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """
        First we don't log leaves for unapproved people.
        then we grab the guild, and from there read the last entry in the audit log.
        """
        # TODO: Verification
        # This needs to be toggle-able once verification is added to settings.
        if "Needs Approval" in [role.name for role in member.roles]:
            return

        join_log = self.bot.api.get_one_setting("2") # Join_log
        if join_log[0]["status"] == "ok":
            logs_channel = await self.bot.fetch_channel(join_log[0]["settings"][2])

            audit_log = [entry async for entry in member.guild.audit_logs(limit=1)][0]

            if str(audit_log.action) != "AuditLogAction.ban" and str(audit_log.action) != "AuditLogAction.kick":
                embed = embed_leave(member)

                await logs_channel.send(embed=embed)



async def setup(bot: commands.Bot) -> None:
    """boink"""
    await bot.add_cog(LoggingLeaves(bot))