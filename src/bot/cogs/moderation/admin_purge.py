"""
Admin command to remove messages in bulk.
"""
import logging
from discord.ext import commands


logger = logging.getLogger(__name__)

class AdminPurge(commands.Cog):
    """
    We are limited to 100 messages per command by Discord API
    TODO: This command should be hidden from non-staff users.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Removes up to 100 messages from channel.")
    @commands.has_permissions(manage_messages=True)
    # TODO: DATABASE ROLES.
    # @commands.has_role("Staff")
    async def purge_messages(self, ctx, number_messages):
        """
        We currently have permissions on this command set,
        which throws an error when the user does not have the correct perms.
        We handle this with an error_handler block
        """
        channel = self.bot.api.get_one_setting("3")  # chat_log
        if channel[0]["status"] == "ok":
            logs_channel = await self.bot.fetch_channel(channel[0]["settings"][2])
            await ctx.channel.purge(limit=int(number_messages))

            if channel[0]["settings"][2] != "0":
                logger.info(f"{ctx.author.name} is purging {number_messages} from the {channel[0]["settings"][1]}")
                await logs_channel.respond(f"{number_messages} messages purged" f" from {ctx.channel.mention}" f" by {ctx.author.mention}.")
            else:
                logger.warning(f"Purge command was used by {ctx.author.name}, but logging for the chat log was turned off.")
        else:
            logger.critical("API error while purging. Status is NOT ok.")

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """
        Handles errors for this cog
        """
        if isinstance(error, commands.MissingPermissions):
            await ctx.channel.send(
                f"Sorry, {ctx.author.name}, you dont have the " f"correct permissions to use this command!",
                reference=ctx.message,
            )

        if isinstance(error, commands.MissingRole):
            await ctx.channel.send(
                f"Sorry, {ctx.author.name}, you do not have the correct role to use this command!",
                reference=ctx.message,
            )


async def setup(bot) -> None:
    """
    required by all cogs.
    """
    await bot.add_cog(AdminPurge(bot))