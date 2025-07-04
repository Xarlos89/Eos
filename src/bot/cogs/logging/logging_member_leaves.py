"""
Logs when a member leaves.
"""
import os
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
        self.verification_role = self.bot.api.get_one_role('6')[0]['roles'][2]  # Verification role ID
        self.join_log = self.bot.api.get_one_log_setting("2")  # Join_log

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """
        First we don't log leaves for unapproved people.
        then we grab the guild, and from there read the last entry in the audit log.
        """
        if member.guild.id != int(os.getenv("MASTER_GUILD")) or \
                member.guild.id is None:
            logger.warning(">> on_member_remove fired, but not in master guild. Ignoring event.")
            return

        if self.verification_role in [role.id for role in member.roles]:
            return

        if self.join_log[0]["status"] == "ok":
            if self.join_log[0]["logging"][2] == "0":
                logger.debug(f"log was triggered, but logging is disabled. API: {self.join_log}")
                return
            logs_channel = await self.bot.fetch_channel(self.join_log[0]["logging"][2])

            audit_log = [entry async for entry in member.guild.audit_logs(limit=1)][0]

            if str(audit_log.action) != "AuditLogAction.ban" and str(audit_log.action) != "AuditLogAction.kick":
                embed = embed_leave(member)

                await logs_channel.send(embed=embed)
        else:
            logger.critical(f"API error. API response not ok. -> {self.join_log}")


async def setup(bot: commands.Bot) -> None:
    """boink"""
    await bot.add_cog(LoggingLeaves(bot))
