"""
A simple catfact command.
"""
import logging

import aiohttp
import requests
from discord.ext import commands

logger = logging.getLogger(__name__)


class CatFact(commands.Cog):
    """
    # Hits the catfact API and returns the response.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="catfact")
    async def catfact(self, ctx):
        """
        Sends a cat fact using an API
        """
        fact = await self.get_catfact()
        if fact is None:
            await ctx.send("Failed to get cat fact.")
        await ctx.send(fact)

    async def get_catfact(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://catfact.ninja/fact") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("fact")
                else:
                    return "Could not get a cat fact."



async def setup(bot):
    """
    Required.
    """
    await bot.add_cog(CatFact(bot))
