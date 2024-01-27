import logging
from discord.ext import commands


logger = logging.getLogger(__name__)


class Health(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command()
    async def healthcheck_api(self, ctx: commands.Context) -> None:
        logger.debug("healthcheck_api command used.")
        await ctx.channel.send(self.bot.api.api_health_check())

    @commands.hybrid_command()
    async def healthcheck_db(self, ctx: commands.Context) -> None:
        logger.debug("healthcheck_db command used.")
        await ctx.channel.send(self.bot.api.database_health_check())


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Health(bot))

