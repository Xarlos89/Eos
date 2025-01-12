"""
Logging for role changes. Logs the user who did the changing, the target user and the role.
"""
import logging
from datetime import datetime
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


def embed_role_add(some_member, member_who_did_action, role_obj):
    """
    Embedding for user kick alerts.
    """
    embed = discord.Embed(
        title=""
        , description=f'<@{member_who_did_action.id}> added <@&{role_obj.id}> to <@{some_member.id}>'
        , color=discord.Color.green()
        , timestamp=datetime.utcnow()
    )
    return embed


def embed_role_remove(some_member, member_who_did_action, role_obj):
    """
    Embedding for user kick alerts.
    """
    embed = discord.Embed(
        title=""
        , description=f'<@{member_who_did_action.id}> removed <@&{role_obj.id}> from <@{some_member.id}>'
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )
    return embed


class LoggingRoles(commands.Cog):
    """
    Simple listener to on_member_update
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """
        Checks what roles were changed, and logs it in the log channel.
        Can be quite spammy.
        """
        audit_log = [entry async for entry in before.guild.audit_logs(limit=1)][0]

        if str(audit_log.action) == "AuditLogAction.member_role_update":
            target_member = audit_log.target
            responsible_member = audit_log.user

            changed_roles = []
            channel = self.bot.api.get_one_setting("4") # User_log
            if channel[0]["status"] == "ok":
                if channel[0]["logging"][2] == "0":
                    logger.debug(f"log was triggered, but logging is disabled. API: {channel}")
                    return
                logs_channel = await self.bot.fetch_channel(channel[0]["logging"][2])

                if len(before.roles) > len(after.roles):
                    for role in before.roles:
                        if role not in after.roles:
                            changed_roles.append(role)
                    for item in changed_roles:
                        embed = embed_role_remove(target_member, responsible_member, item)
                        await logs_channel.send(embed=embed)

                elif len(before.roles) < len(after.roles):
                    for role in after.roles:
                        if role not in before.roles:
                            changed_roles.append(role)
                    for item in changed_roles:
                        embed = embed_role_add(target_member, responsible_member, item)
                        await logs_channel.send(embed=embed)
            else:
                logger.critical(f"API error. API response not ok. -> {channel}")



async def setup(bot: commands.Bot) -> None:
    """boink"""
    await bot.add_cog(LoggingRoles(bot))