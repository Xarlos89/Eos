import logging
import discord
from discord.ext import commands
from datetime import datetime

logger = logging.getLogger(__name__)


def channel_embed(audit_log, message):
    embed = discord.Embed(
        title='<:red_circle:1043616578744357085> Deleted Message'
        , description=f'{audit_log.user} deleted a message'
                      f'\nIn {audit_log.channel}\nMessage '
                      f'author: {audit_log.author}'
        , color=discord.Color.dark_red()
        , timestamp=datetime.utcnow()
    )

    embed.set_thumbnail(
        url=audit_log.user.avatar  # the person who DELETED the message
    )
    if len(message.content) > 1020:
        the_message = message.content[0:1020] + '...'
    else:
        the_message = message.content
    embed.add_field(
        name='Message: '
        , value=the_message
        , inline=True
    )
    return embed


class LogMessages(commands.Cog):
    """
    Simple listener to on_message_delete
    then checks the audit log for exact details
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """
        If a mod deletes, take the audit log event. If a user deletes, handle it normally.
        """
        audit_log = [entry async for entry in message.guild.audit_logs(limit=1)][0]

        if str(audit_log.action) == 'AuditLogAction.message_delete':
            """            
            If the audit log is triggered, it means someone OTHER than the author deleted the message.
            https://discordpy.readthedocs.io/en/stable/api.html?highlight=audit%20log#discord.AuditLogAction.message_delete
            """
            logger.info(f"Moderator ({audit_log.user.name}) removed message in {message.channel}")
            # TODO: Replace log channel with entry in the DB.
            # embed = channel_embed(audit_log, message)
            # await logs_channel.send(embed=channel_embed(audit_log, message))

            return

        else:
            logger.info(f"{message.author.name} deleted a message in {message.channel}")
            # TODO: Replace log channel with entry in the DB.
            # await logs_channel.send(f"{message.author.mention}", embed=channel_embed(message.author, message))

            return


async def setup(bot: commands.Bot) -> None:
    """
    Necessary for loading the cog into the bot instance.
    """
    await bot.add_cog(LogMessages(bot))
