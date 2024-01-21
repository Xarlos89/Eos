import logging
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


class MessageListener(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.message) -> None:
        if not message.author.bot:
            logger.debug('Message has been sent.')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MessageListener(bot))
