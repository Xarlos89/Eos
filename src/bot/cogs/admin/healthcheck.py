import logging
from discord.ext import commands


logger = logging.getLogger(__name__)


class Health(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command()
    async def healthcheck(self, ctx: commands.Context) -> None:
        logger.debug("healthcheck command used.")
        await ctx.channel.send(self.bot.api.healthcheck())

    @commands.hybrid_command()
    async def all_commands(self, ctx: commands.Context) -> None:
        logger.debug("all_commands command used.")
        await ctx.channel.send(self.bot.api.all_commands())


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Health(bot))

