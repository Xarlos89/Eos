import logging
import discord
from discord.ext import commands

from core.embeds import embed_info, embed_hc

logger = logging.getLogger(__name__)


class Points(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command()
    async def sync_users(self, ctx: commands.Context) -> None:
        pass

    @commands.hybrid_command()
    async def get_points(self, ctx: commands.Context, user: discord.Member) -> None:
        points = self.bot.api.get_points(user.id)
        if points['status'] == 'ok':
            await ctx.reply(f"{user.display_name} has {points['points'][0]} points")
        else:
            await ctx.reply(f"Oopsie. Unexpected error. Check the logs.")
            logger.critical(points)

    @commands.hybrid_command()
    async def add_points(self, ctx: commands.Context, user: discord.User, amount) -> None:
        update_points = self.bot.api.update_points(user.id, int(amount))
        if update_points['status'] == 'ok':
            await ctx.reply(f"{amount} points {'removed from' if amount.startswith('-') else 'added to'} to {user.display_name}")
        else:
            await ctx.reply(f"Oopsie. Unexpected error. Check the logs.")
            logger.critical(update_points)



    @commands.hybrid_command()
    async def remove_points(self, ctx: commands.Context, user: discord.User) -> None:
        pass




async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Points(bot))
