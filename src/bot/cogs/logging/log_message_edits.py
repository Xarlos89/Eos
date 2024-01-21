import logging
import discord
from discord.ext import commands
from datetime import datetime

logger = logging.getLogger(__name__)


def channel_embed(author, message_before, message_after) -> discord.Embed:
    """
    Building the embed object when an event is detected.
    This is only here to keep the actual event cleaner, and easier to read.
    :param author: discord.member object
    :param username_before:  The discord.member.name or .nickname of the user before.
    :param username_after:  The discord.member.name or .nickname of the user after.
    :return: discord.Embed object
    """
    embed = discord.Embed(
        title='<:orange_circle:1043616962112139264> Message Edit'
        , description=f'Edited by {author.name}\n'
                      f'In {message_after.channel.mention}'
        , color=discord.Color.dark_orange()
        , timestamp=datetime.utcnow()
    )
    if author.avatar is not None:
        embed.set_thumbnail(
            url=author.avatar
        )

    embed.add_field(
        name='Original message: '
        , value=message_before.content[:1000]
        , inline=False
    )

    embed.add_field(
        name='After editing: '
        , value=message_after.content[:1000]
        , inline=False
    )
    return embed


class LogMessageEdits(commands.Cog):
    """
    Simple listener to on_message_edit
    """

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after) -> None:

        # IGNORE /run, since we will set up an on_message_edit handler there with opposite logic
        if message_before.content.startswith('/run') or message_after.content.startswith('/run'):
            return

        elif message_before.content != message_after.content:
            # This guy here makes sure we use the displayed name inside the guild.
            if message_before.author.nick is None:
                username = message_before.author
            else:
                username = message_before.author.nick

            author = message_before.author

            logger.info(f"{username} edited a message in {message_before.channel}")
            logger.debug(f" - Message Before: {message_before.content}")
            logger.debug(f" - Message After: {message_after.content}")

            # TODO: Replace log channel with entry in the DB.
            # logs_channel = await self.bot.fetch_channel(self.bot.server_settings.log_channel["chat_log"])
            # await logs_channel.send(embed=channel_embed)
            return


async def setup(bot: commands.Bot) -> None:
    """
    Necessary for loading the cog into the bot instance.
    """
    await bot.add_cog(LogMessageEdits(bot))
