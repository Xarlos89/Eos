"""
Logging for message deletes
"""
import logging
from datetime import datetime
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


def embed_message_delete(some_member, some_message, some_moderator=None):
    """
    Embedding for user message deletion alerts.
    """
    embed = discord.Embed(
        title=f'<:red_circle:1043616578744357085> Deleted Message'
        , description=f'{some_moderator.mention if some_moderator is not None else some_member.mention} deleted a message'
                      f'\nIn {some_message.channel}\nMessage '
                      f'author: {some_member.mention}'
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )

    embed.set_thumbnail(
        url=some_member.avatar if some_moderator is None else some_moderator.avatar  # the person who DELETED the message
    )
    if len(some_message.content) > 1020:
        the_message = some_message.content[0:1020] + '...'
    else:
        the_message = some_message.content
    embed.add_field(
        name='Message: '
        , value=the_message
        , inline=True
    )

    return embed


class LoggingMessageDelete(commands.Cog):
    """
    Simple listener to on_message_delete
    then checks the audit log for exact details
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        # TODO: Do not log in Staff channels.
        """
        If a mod deletes, take the audit log event. If a user deletes, handle it normally.
        """
        audit_log = [entry async for entry in message.guild.audit_logs(limit=1)][0]
        channel = self.bot.api.get_one_log_setting("3") # chat_log
        if channel[0]["status"] == "ok":
            if channel[0]["logging"][2] == "0":
                logger.debug(f"log was triggered, but logging is disabled. API: {channel}")
                return
            logs_channel = await self.bot.fetch_channel(channel[0]["logging"][2])

            if str(audit_log.action) == 'AuditLogAction.message_delete':
                # Then a moderator deleted a message.
                embed = embed_message_delete(audit_log.target, message, audit_log.user)
                await logs_channel.send(embed=embed)

            else:
                # Otherwise, the author deleted it.
                username = message.author
                await logs_channel.send(embed=embed_message_delete(username, message))
        else:
            logger.critical(f"API error. API response not ok. -> {channel}")


async def setup(bot: commands.Bot) -> None:
    """boink"""
    await bot.add_cog(LoggingMessageDelete(bot))