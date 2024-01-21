import logging
import discord
from discord.ext import commands
from datetime import datetime

logger = logging.getLogger(__name__)


def channel_embed(before, after) -> discord.Embed:
    """
    Building the embed object when an event is detected.
    This is only here to keep the actual event cleaner, and easier to read.

    :param username_before:  The discord.member.name or .nickname of the user before.
    :param username_after:  The discord.member.name or .nickname of the user after.
    :return: discord.Embed object
    """

    embed = discord.Embed(
        title=f'{before} updated their profile picture!'
        , color=discord.Color.dark_grey()
        , timestamp=datetime.utcnow()
    )

    embed.set_thumbnail(
        url=after.avatar
    )

    return embed


class LogAvatars(commands.Cog):
    """
    Simple listener to on_user_update
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        """
        if the avatar before is != to the avatar after, do stuff.
        """
        logger.info(f"{before.name} updated their avatar.")

        # This is from Zorak.
        # TODO: Replace log channel with entry in the DB.
        # if before.avatar != after.avatar:
        #     logs_channel = await self.bot.fetch_channel(self.bot.server_settings.log_channel["mod_log"])
        #     await logs_channel.send(embed=channel_embed)
        return


async def setup(bot: commands.Bot) -> None:
    """
    Necessary for loading the cog into the bot instance.
    """
    await bot.add_cog(LogAvatars(bot))
