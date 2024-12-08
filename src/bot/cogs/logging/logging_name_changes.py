"""
logs when a username is changed.
"""
import logging
from datetime import datetime
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


def embed_name_change(username_before, username_after):
    """
    Embedding for user name change alerts.
    """
    embed = discord.Embed(
        title=""
        , description=f"{username_before} changed their name to {username_after}"
        , color=discord.Color.dark_grey()
        , timestamp=datetime.utcnow()
    )
    return embed


class LoggingNameChanges(commands.Cog):
    """
    Simple listener to on_member_update
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
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
            channel = self.bot.api.get_one_setting("4") # User_log
            if channel[0]["status"] == "ok":
                if channel[0]["settings"][2] == "0":
                    return
                logs_channel = await self.bot.fetch_channel(channel[0]["settings"][2])

                embed = embed_name_change(username_before, username_after)

                await logs_channel.send(f"{username_after.mention}", embed=embed)
            else:
                logger.critical(f"API error. API response not ok. -> {channel}")



async def setup(bot: commands.Bot) -> None:
    """boink"""
    await bot.add_cog(LoggingNameChanges(bot))