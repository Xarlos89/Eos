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
        await ctx.send(f"That command does not exist. Try again.\n {error}")

        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            logger.info(f"ERROR: {ctx.guild.name} -- {ctx.author} -- {error}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CommandListener(bot))
