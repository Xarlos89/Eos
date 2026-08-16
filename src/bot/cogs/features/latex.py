"""
LaTeX command to generate mathematical equations.
"""

import logging
from pathlib import Path

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from ..constants import BG_COLORS, TXT_COLORS

logger = logging.getLogger(__name__)


def embed_info(title, message, image_path=None):
    """
    Embedding for general things
    """
    embed = discord.Embed(
        title=title, description=message, color=discord.Color.dark_purple()
    )
    if image_path:
        embed.set_image(url=image_path)
    return embed


class LaTeX(commands.Cog):
    """
    # Grabs the svg code from codecogs API and converts it to a png for display in an embed.
    """

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def latex_bg(self, ctx):
        file = discord.File(
            Path.cwd().joinpath("src", "bot", "static", "images", "bg_colors.png"),
            filename="bg_colors.png",
        )
        embed = embed_info(
            "LaTeX Background Colors",
            "The following colors are available:",
            "attachment://bg_colors.png",
        )
        await ctx.respond(file=file, embed=embed, ephemeral=True)

    @app_commands.command()
    async def latex_txt(self, ctx):
        file = discord.File(
            Path.cwd().joinpath("src", "bot", "static", "images", "txt_colors.png"),
            filename="txt_colors.png",
        )
        embed = embed_info(
            "LaTeX Text Colors",
            "The following colors are available:",
            "attachment://txt_colors.png",
        )
        await ctx.respond(file=file, embed=embed, ephemeral=True)

    @app_commands.command()
    async def latex(
        self,
        ctx,
        equation: str,
        *,
        bg_color: str = "black",
        txt_color: str = "White",
        dpi: int = 200,
    ):
        """
        Send a mathematical equation using LaTeX commands

        Parameters
        ----------
        equation : LaTeX equation (do not include $ on both ends)
        bg_color : Use `/latex_bg` to see available colors. Default is "black"
        txt_color : Use '/latex_txt' to see available colors. Default is "White"
        dpi : Choose an image size. Default is 200
        """
        logger.info("%s used the %s command.", ctx.author.name, ctx.command)

        # check for valid user specified color for text and background
        bg_color = bg_color.strip().lower().replace(" ", "")
        txt_color = txt_color.strip().title().replace(" ", "")

        if bg_color not in BG_COLORS:
            bg_color = "black"
        if txt_color not in TXT_COLORS:
            txt_color = "White"

        # handle necessary character replacements
        escape_characters = {
            "\n": r"\n",
            "\r": r"\r",
            "\t": r"\t",
            "\x08": r"\b",
            "\x0c": r"\f",
            "\x0b": r"\v",
            "\x07": r"\a",
            " ": "&space;",
        }

        for e, c in escape_characters.items():
            equation = equation.replace(e, c)

        # prevent user specified dpi from being too big
        dpi = min(int(dpi), 500)

        image_path = (
            r"https://latex.codecogs.com/png.image?\dpi{"
            + f"{dpi}"
            + r"}\bg{"
            + bg_color
            + r"}\color{"
            + txt_color
            + "}"
            + equation
        )

        if await self.latex_available(image_path):
            embed = embed_info(
                "LaTeX",
                equation.replace("&space;", " "),
                image_path,
            )
            # Send the embed with the image
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("Failed to fetch the image from the API", ephemeral=True)

    async def latex_available(self, image_path):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_path) as response:
                    return response.status == 200
        except aiohttp.ClientError:
            logger.exception("Failed to fetch LaTeX image from CodeCogs")
            return False


async def setup(bot):
    """
    Required.
    """
    await bot.add_cog(LaTeX(bot))
