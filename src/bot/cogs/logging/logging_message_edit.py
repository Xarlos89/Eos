"""
Logging for message edits
"""
import logging
from datetime import datetime
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


def embed_message_edit(some_username, orig_author, some_message_before, some_message_after):
    """
    Embedding for user message edit alerts.
    """
    embed = discord.Embed(
        title=""
        , description=f'Message Edited by {some_username}\n'
                      f'In {some_message_after.channel.mention}'
        , color=discord.Color.dark_orange()
        , timestamp=datetime.utcnow()
    )
    if orig_author.avatar is not None:
        embed.set_thumbnail(
            url=orig_author.avatar
        )

    embed.add_field(
        name='Original message: '
        , value=some_message_before.content[:1000]
        , inline=True
    )

    embed.add_field(
        name='After editing: '
        , value=some_message_after.content[:1000]
        , inline=True
    )

    return embed


class LoggingMessageEdit(commands.Cog):
    """
    Simple listener to on_message_edit
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        # TODO: Do not log in Staff channels.

        # Ignore any bot messages
        if message_before.author.bot or message_after.author.bot:
            return

        # IGNORE /run, since we will set up an on_message_edit handler there with opposite logic
        if message_before.content.startswith('/run') or message_after.content.startswith('/run'):
            return

        elif message_before.content != message_after.content:
            channel = self.bot.api.get_one_log_setting("3")  # chat_log
            if channel[0]["status"] == "ok":
                if channel[0]["logging"][2] == "0":
                    logger.debug(f"log was triggered, but logging is disabled. API: {channel}")
                    return

                logs_channel = await self.bot.fetch_channel(channel[0]["logging"][2])

                # This guy here makes sure we use the displayed name inside the guild.
                if message_after.author.nick is None:
                    username = message_after.author
                else:
                    username = message_after.author.nick

                author = message_after.author

                embed = embed_message_edit(username, author, message_before, message_after)
                await logs_channel.send(embed=embed)

            else:
                logger.critical(f"API error. API response not ok. -> {channel}")


async def setup(bot: commands.Bot) -> None:
    """boink"""
    await bot.add_cog(LoggingMessageEdit(bot))