import logging
import discord
from discord.ext import commands
from datetime import datetime

logger = logging.getLogger(__name__)


def embed_unban(some_member) -> discord.Embed:
    """
    Embedding for user un-ban alerts.

    :param some_member: discord.Member
        - The member being unbaned
    """
    embed = discord.Embed(
        title='<:green_circle:1046088647759372388> User Un-Banned'
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )

    embed.add_field(
        name=f'{some_member.name} was un-banned.'
        , value='Welcome back.'
        , inline=True
    )

    return embed


class LogUnbans(commands.Cog):
    """
    Simple listener to on_member_unban
    """

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_unban(self, member) -> None:
        """
        Just listen for the event, embed it, and send it off.
        """
        embed = embed_unban(member)

        logger.info(f"{member.name} was unbanned in {member.guild}")
        # TODO: Update this to pull form DB!
        # logs_channel = await self.bot.fetch_channel(self.bot.server_settings.log_channel["mod_log"])
        # await logs_channel.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """
    Necessary for loading the cog into the bot instance.
    """
    await bot.add_cog(LogUnbans(bot))
