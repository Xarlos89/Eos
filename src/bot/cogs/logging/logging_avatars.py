"""
Logs user avatar changes.
TODO: Would be cool to add an API that detects nasty images here.
"""
import logging
from datetime import datetime
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


def embed_avatar(before, after):
    """
    Embedding for avatar change alerts.
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


class LoggingAvatars(commands.Cog):
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
        if before.avatar != after.avatar:
            channel = self.bot.api.get_one_setting("4") # User_log
            if channel[0]["status"] == "ok":
                if channel[0]["settings"][2] == "0":
                    return
                logs_channel = await self.bot.fetch_channel(channel[0]["settings"][2])

                embed = embed_avatar(before, after)

                await logs_channel.send(embed=embed)
            else:
                logger.critical(f"API error. API response not ok. -> {channel}")


async def setup(bot: commands.Bot) -> None:
    """boink"""
    await bot.add_cog(LoggingAvatars(bot))