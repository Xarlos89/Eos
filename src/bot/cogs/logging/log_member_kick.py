import logging
import discord
from discord.ext import commands
from datetime import datetime


logger = logging.getLogger(__name__)


def embed_kick(some_member, audit_log_entry) -> discord.Embed:
    """
    Embedding for user kick alerts.

    :param some_member: discord.Member
        - The member being kicked
    :param audit_log_entry: discord.AuditLogEntry
        - The audit log entry of the event
    """
    embed = discord.Embed(
        title=f'<:red_circle:1043616578744357085> {some_member} was kicked'
        , description=f'By: {audit_log_entry.user}'
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )

    embed.add_field(
        name='Reason:'
        , value=f'{audit_log_entry.reason}'
        , inline=True
    )

    return embed


class LogKicks(commands.Cog):
    """
    Simple listener to on_member_remove
    then checks the audit log for exact details
    """

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member) -> None:
        """
        First we don't log kicks for unapproved people.
        then we grab the guild, and from there read the last entry in the audit log.
        """

        # TODO: [verification!] - Update this to pull form DB!
        # if "Needs Approval" in [role.name for role in member.roles]:
        #     return

        audit_log = [entry async for entry in member.guild.audit_logs(limit=1)][0]

        if str(audit_log.action) == "AuditLogAction.kick":
            if audit_log.target == member:
                embed = embed_kick(member, audit_log)

                logger.info(f"{member.name} was kicked from {member.guild.name} by {audit_log.user.name}")
                # TODO: Update this to pull form DB!
                # logs_channel = await self.bot.fetch_channel(self.bot.server_settings.log_channel["mod_log"])
                # await logs_channel.send(embed=embed)
                return


async def setup(bot: commands.Bot) -> None:
    """
    Necessary for loading the cog into the bot instance.
    """
    await bot.add_cog(LogKicks(bot))
