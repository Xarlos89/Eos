import logging
import discord
from discord.ext import commands

from core.embeds import embed_info, embed_hc

logger = logging.getLogger(__name__)


class Health(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command()
    async def hc(self, ctx: commands.Context) -> None:
        logger.debug("healthcheck command used.")

        hc_api = self.bot.api.api_health_check()
        try:
            status_api = hc_api[0]['status']
            status_code_api = hc_api[1]
        except KeyError as api_ded:
            status_api = "Unhealthy"
            status_code_api = "API Unreachable"

        api_info = {
                'message': f"API Status: {status_api}"
                , 'status_code': f"Response: {status_code_api}"
                , 'color': discord.Color.green() if status_api == 'ok' else discord.Color.red()
                }

        hc_db = self.bot.api.database_health_check()
        try:
            status_db = hc_db[0]['status']
            status_code_db = hc_db[1]
        except KeyError as api_ded:
            status_db = "Unhealthy"
            status_code_db = "DB Unreachable"

        db_info = {
                'message': f"Database Status: {status_db}"
                , 'status_code': f"Response: {status_code_db}"
                , 'color': discord.Color.green() if status_db == 'ok' else discord.Color.red()
                }

        await ctx.reply(
            embed=embed_hc(api_info, db_info))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Health(bot))
