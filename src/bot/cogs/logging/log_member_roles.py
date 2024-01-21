import logging
import discord
from discord.ext import commands
from datetime import datetime

logger = logging.getLogger(__name__)


def embed_role_add(some_member, member_who_did_action, role_obj) -> discord.Embed:
    """
    Embedding for user kick alerts.

    :param some_member: discord.Member
        - The receiver of the action
    :param member_who_did_action: discord.Member
        - The person who did the action
    :param role_obj: discord.Role
        - The role in question
    """
    embed = discord.Embed(
        title=':green_square: Role Update'
        , description=f'<@{member_who_did_action.id}> added a role to <@{some_member.id}> '
        , color=discord.Color.green()
        , timestamp=datetime.utcnow()
    )

    embed.add_field(
        name='Added role:'
        , value=f'<@&{role_obj.id}>'
        , inline=True
    )
    return embed


def embed_role_remove(some_member, member_who_did_action, role_obj) -> discord.Embed:
    """
    Embedding for user kick alerts.

    :param some_member: discord.Member - The receiver of the action
    :param member_who_did_action: discord.Member - The person who did the action
    :param role_obj: discord.Role - The role in question
    """
    embed = discord.Embed(
        title=':negative_squared_cross_mark: Role Update'
        , description=f'<@{member_who_did_action.id}> removed a role from <@{some_member.id}>'
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )

    embed.add_field(
        name='Removed role:'
        , value=f'<@&{role_obj.id}>'
        , inline=True
    )
    return embed


class LoggingRoles(commands.Cog):
    """
    Simple listener to on_member_update
    """

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after) -> None:
        """
        Checks what roles were changed, and logs it in the log channel.
        Can be quite spammy.
        """
        audit_log = [entry async for entry in before.guild.audit_logs(limit=1)][0]

        if str(audit_log.action) == "AuditLogAction.member_role_update":
            target_member = audit_log.target
            responsible_member = audit_log.user

            changed_roles = []
            # TODO: Replace log channel with entry in the DB.
            # logs_channel = await self.bot.fetch_channel(self.bot.server_settings.log_channel["mod_log"])
            if len(before.roles) > len(after.roles):
                for role in before.roles:
                    if role not in after.roles:
                        changed_roles.append(role)
                for item in changed_roles:
                    embed = embed_role_remove(target_member, responsible_member, item)
                    logging.info(f"{responsible_member.name} removed {item} from {target_member.name}")
                    # await logs_channel.send(embed=embed)

            elif len(before.roles) < len(after.roles):
                for role in after.roles:
                    if role not in before.roles:
                        changed_roles.append(role)
                for item in changed_roles:
                    embed = embed_role_add(target_member, responsible_member, item)
                    logging.info(f"{responsible_member.name} added {item} to {target_member.name}")
                    # await logs_channel.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """
    Necessary for loading the cog into the bot instance.
    """
    await bot.add_cog(LoggingRoles(bot))
