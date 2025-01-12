"""
Admin command to remove messages in bulk.
"""
import logging
from discord.ext import commands


logger = logging.getLogger(__name__)


def embed_info(message):
    """
    Embedding for general things
    """
    embed = discord.Embed(
        title=''
        , description=message
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )
    return embed

async def is_moderator(ctx) -> bool:
    """
    Check if the context user has moderator permissions
    https://discordpy.readthedocs.io/en/stable/api.html?highlight=guild_permissions#discord.Permissions.manage_messages
    """
    return ctx.message.author.guild_permissions.manage_messages



class AdminPurge(commands.Cog):
    """
    We are limited to 100 messages per command by Discord API
    TODO: This command should be hidden from non-staff users.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.check(is_moderator)
    @commands.command(description="Removes up to 100 messages from channel.")
    async def purge_messages(self, ctx, number_messages):
        """
        We currently have permissions on this command set,
        which throws an error when the user does not have the correct perms.
        We handle this with an error_handler block
        """
        channel = self.bot.api.get_one_setting("3")  # chat_log
        if channel[0]["status"] == "ok":
            logs_channel = await self.bot.fetch_channel(channel[0]["logging"][2])
            await ctx.channel.purge(limit=int(number_messages))

            if channel[0]["logging"][2] != "0":
                logger.info(f"{ctx.author.name} is purging {number_messages} from the {channel[0]["logging"][1]}")
                await logs_channel.respond(f"{number_messages} messages purged" f" from {ctx.channel.mention}" f" by {ctx.author.mention}.")
            else:
                logger.warning(f"Purge command was used by {ctx.author.name}, but logging for the chat log was turned off.")
        else:
            logger.critical("API error while purging. Status is NOT ok.")

    @purge_messages.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.channel.send(embed=embed_info(
                f"{ctx.author.mention}, you dont have permission to purge messages. The staff has been notified."))


async def setup(bot) -> None:
    """
    required by all cogs.
    """
    await bot.add_cog(AdminPurge(bot))