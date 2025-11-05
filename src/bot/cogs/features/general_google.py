"""
A simple sarcastic google command.
"""

import logging

from discord.ext import commands


logger = logging.getLogger(__name__)


class GeneralSarcasticGoogle(commands.Cog):
    """
    # Creates a link to the Let me google that for you site.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="google")
    async def google(self, ctx, question):
        """
        sarcastically googles a question.
        """
        logger.info("%s used the %s command.", ctx.author.name, ctx.command)
        await ctx.send(
            f"Here, allow me to google that one for you:"
            f"\nhttps://letmegooglethat.com/?q={question.replace(' ', '+')}"
        )


async def setup(bot):
    """
    Required.
    """
    await bot.add_cog(GeneralSarcasticGoogle(bot))
