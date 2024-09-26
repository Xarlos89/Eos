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
        added = 0
        for user in ctx.guild.members:
            self.bot.api.add_user_to_points(user.id)
            added += 1
        await ctx.reply(
            embed=embed_info(
                ""
                , f"Added {added} users"
                , discord.Color.lighter_gray()
            )
        )

    @commands.hybrid_command()
    async def get_points(self, ctx: commands.Context, user: discord.Member) -> None:
        points = self.bot.api.get_points(user.id)
        if points['status'] == 'ok':
            await ctx.reply(
                embed=embed_info(
                    ""
                    , f"{user.display_name} has {points['points'][0]} points"
                    , discord.Color.lighter_gray()
                )
            )
        else:
            await ctx.reply("Oopsie. Unexpected error. Check the logs.")
            logger.critical(points)

    @commands.hybrid_command()
    async def update_points(self, ctx: commands.Context, user: discord.User, amount) -> None:
        update_points = self.bot.api.update_points(user.id, int(amount))
        if update_points['status'] == 'ok':
            await ctx.reply(
                embed=embed_info(
                    ""
                    , f"{amount} points {'removed from' if amount.startswith('-') else 'added to'} to {user.display_name}"
                    , discord.Color.green() if not amount.startswith('-') else discord.Color.red()
                )
            )
        else:
            await ctx.reply(f"Oopsie. Unexpected error. Check the logs.")
            logger.critical(update_points)

    @commands.hybrid_command()
    async def top_10(self, ctx: commands.Context) -> None:
        top10 = self.bot.api.top_10()
        if top10['status'] == 'ok':

            data = []
            for user in top10['message']:
                user_obj = self.bot.get_user(int(user[0]))
                data.append((user_obj.display_name, user[1]))

            await ctx.reply(
                embed=embed_info(
                    "Top 10 Point Earners"
                    , "\n".join([f"{index + 1}. {user_name} - {points}"
                              for index, (user_name, points) in enumerate(data)])
                    , discord.Color.yellow()
                )
            )
        else:
            await ctx.reply(f"Oopsie. Unexpected error. Check the logs.")
            logger.critical(top10)

    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        if message.author.bot:
            return
        msg = message.content.split()
        logger.debug(f"Updating {len(msg)} points for {message.author.display_name} for sending a message.")
        self.bot.api.update_points(message.author.id, int(len(msg)))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        msg = message.content.split()
        logger.debug(f"Updating -{len(msg)} points for {message.author.display_name} for deleting a message.")
        self.bot.api.update_points(message.author.id, int(len(msg))*-1)

    @commands.Cog.listener()
    async def on_member_join(self, member) -> None:
        logger.debug(f"Adding {member.display_name} to the points DB.")
        self.bot.api.add_user_to_points(member.id)

    @commands.Cog.listener()
    async def on_member_remove(self, member) -> None:
        logger.debug(f"Removing {member.display_name} from the points DB.")
        self.bot.api.delete_member(member.id)

    @update_points.error
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(
                embed=embed_info(
                    "Error!", "You must provide a required argument."
                    , discord.Color.dark_gray()
                )
            )

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Points(bot))
