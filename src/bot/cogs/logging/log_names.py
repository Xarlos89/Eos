import logging
import discord
from discord.ext import commands
from datetime import datetime

logger = logging.getLogger(__name__)


def channel_embed(username_before, username_after) -> discord.Embed:
    """
    Building the embed object when an event is detected.
    This is only here to keep the actual event cleaner, and easier to read.

    :param username_before:  The discord.member.name or .nickname of the user before.
    :param username_after:  The discord.member.name or .nickname of the user after.
    :return: discord.Embed object
    """
    embed = discord.Embed(
        title='<:grey_exclamation:1044305627201142880> Name Change'
        , description=f'Changed by: {username_before}.'
        , color=discord.Color.dark_grey()
        , timestamp=datetime.utcnow()
    )

    embed.set_thumbnail(
        url=username_after.avatar
    )

    embed.add_field(
        name='Before'
        , value=username_before
        , inline=True
    )

    embed.add_field(
        name='After'
        , value=username_after
        , inline=True
    )

    return embed


class LogNames(commands.Cog):
    """
    Simple listener to on_member_update
    """

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after) -> None:
        """
        Just checking if the name before is != to the name after.
        """
        if before.nick is None:
            username_before = before
        else:
            username_before = before.nick

        if after.nick is None:
            username_after = after
        else:
            username_after = after.nick

        if before.nick != after.nick and before.nick is not None:
            logger.info(f"{username_before} changed their name to {username_after}")

            # TODO: Replace log channel with entry in the DB.
            # await logs_channel.send(f"{username_after.mention}", embed=channel_embed(username_before, username_after))
            return


async def setup(bot: commands.Bot) -> None:
    """
    Necessary for loading the cog into the bot instance.
    """
    await bot.add_cog(LogNames(bot))
