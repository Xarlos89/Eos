import logging
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class CommandListener(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener(name='on_command')
    async def log_commands(self, ctx):
        logger.info(f'{ctx.guild.name} -- {ctx.author} -- Used {ctx.command}')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error) -> None:
        """
        This is an error handler for command errors.
        For a list of command errors -> https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#exceptions
        """
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            logger.warning(f"ERROR: {ctx.guild.name} -- {ctx.author} -- {error}")
            await ctx.send(f"That command does not exist. Try again.\n {error}")
            return

        if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            logger.warning(f"ERROR: {ctx.guild.name} -- {ctx.author} -- {error}")
            await ctx.send(f"There was an issue with the command.\nError: {error}")
            return

        logger.critical(f"Error: {error}\n"
                        f"Type: {type(error)}")

        await ctx.send(f"Unhandled Error!\n"
                       f"Maybe we should add this to the error handler?\n"
                       f"Error: {error}\n"
                       f"Type: {type(error)}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CommandListener(bot))
