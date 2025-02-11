"""
Admin command to remove messages in bulk.
"""
import logging
from datetime import datetime
import discord
from discord.ext import commands
from discord import app_commands

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


def api_request_is_ok(request):
    if request[0]["status"] == "ok":
        return True
    return False


def logging_is_activated(request):
    if request[0]["logging"][2] == "0":
        return False
    return True


class AdminPurge(commands.Cog):
    """
    We are limited to 100 messages per command by Discord API
    TODO: This command should be hidden from non-staff users.
    """

    def __init__(self, bot):
        self.bot = bot
        self.log_channel_req = self.bot.api.get_one_log_setting("3")  # chat_log

    @commands.check(is_moderator)
    @app_commands.command(description="Removes up to 100 messages from channel.")
    async def purge_messages(self, interaction: discord.Interaction, number_messages: str):
        """
        We currently have permissions on this command set,
        which throws an error when the user does not have the correct perms.
        We handle this with an error_handler block
        """

        if api_request_is_ok(self.log_channel_req):
            logger.info(f"{interaction.user.name} is purging {number_messages} messages from "
                        f"the {self.log_channel_req[0]['logging'][1]}")
            await interaction.response.defer()
            await interaction.channel.purge(limit=int(number_messages) + 1)

            if logging_is_activated(self.log_channel_req):
                logging_channel = await self.bot.fetch_channel(self.log_channel_req[0]["logging"][2])

                await logging_channel.send(f"{number_messages} messages purged"
                                           f" from {interaction.channel.mention}"
                                           f" by {interaction.user.mention}.")

            elif not logging_is_activated(self.log_channel_req):
                logger.warning(f"Purge command was used by {interaction.user.name}, but "
                               f"logging for the chat log was turned off.")
        else:
            logger.critical("API error while purging messages. Status is NOT ok.")

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
