import logging
from datetime import datetime
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


def embed_info(title, message, color):
    """
    Embedding for avatar change alerts.
    """
    embed = discord.Embed(
        title=f'{title}'
        , description=f'{message}'
        , color=color
        , timestamp=datetime.utcnow()
    )
    return embed

async def is_admin(ctx) -> bool:
    """ Check if the context user has admin permissions"""
    return ctx.message.author.guild_permissions.administrator


class Points(commands.Cog):
    """
    This cog manages a points-based system for Discord guild members.

    It provides the following functionalities:
    - Synchronizes users with a points database.
    - Retrieves and displays a user's points.
    - Updates a user's points (supports adding and subtracting points).
    - Displays the top 10 users with the highest points.
    - Automatically awards points based on message content and deducts points when messages are deleted.
    - Adds users to the database when they join the guild and removes them when they leave.

    The cog interacts with an external API to store and manage user points and includes error handling and logging for various operations.
    """
    def __init__(self, bot: commands.Bot) -> None:
        """Initialization of the points Class"""
        self.bot = bot

    @commands.check(is_admin)
    @commands.hybrid_command()
    async def sync_users(self, ctx: commands.Context) -> None:
        """
        Synchronise users to the points table in the DB
        Users that exist in the DB will not be synced.
        """
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
        """
        Gets the points of a specific member. Takes a Mention, returns an embed.
        """
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

    @commands.check(is_admin)
    @commands.hybrid_command()
    async def update_points(self, ctx: commands.Context, user: discord.User, amount) -> None:
        """
        Updates the points of a specific member. Takes a Mention and an amount, returns an embed.
        Amount can be a positive or negative integer
        """
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
        """
        Gets the top 10 users in the DB with the most points.
        Takes no args, returns an embed.
        """
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
        """
        Listens for messages, splits messages into # of words and gives the author
        that many points.
        """
        if message.author.bot:
            return
        msg = message.content.split()
        logger.debug(f"Updating {len(msg)} points for {message.author.display_name} for sending a message.")
        self.bot.api.update_points(message.author.id, int(len(msg)))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """
        Listens for deleted messages, splits messages into # of words and removes
        that many points from the author
        """
        if message.author.bot:
            return
        msg = message.content.split()
        logger.debug(f"Updating -{len(msg)} points for {message.author.display_name} for deleting a message.")
        self.bot.api.update_points(message.author.id, int(len(msg))*-1)

    @commands.Cog.listener()
    async def on_member_join(self, member) -> None:
        """
        On user join, add them to the database
        """
        logger.debug(f"Adding {member.display_name} to the points DB.")
        self.bot.api.add_user_to_points(member.id)

    @commands.Cog.listener()
    async def on_member_remove(self, member) -> None:
        """
        On user leave/kick/ban, remove them from the database
        """
        logger.debug(f"Removing {member.display_name} from the points DB.")
        self.bot.api.delete_user_from_points(member.id)

    @update_points.error
    async def on_command_error(self, ctx: commands.Context, error):
        """
        Error handling for the >update_points command.
        """
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(
                embed=embed_info(
                    "Error!", "You must provide a required argument."
                    , discord.Color.dark_gray()
                )
            )

async def setup(bot: commands.Bot) -> None:
    """boink"""
    await bot.add_cog(Points(bot))
