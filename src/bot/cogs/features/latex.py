"""
LaTeX command to generate mathematical equations.
"""

import logging
from pathlib import Path

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from ..constants import LATEX_COLORS
from ._latex_utilities import LatexView

logger = logging.getLogger(__name__)


def embed_info(title: str, message: str, image_url: str | None = None) -> discord.Embed:
    """
    Embedding for general things
    """
    embed = discord.Embed(
        title=title, description=message, color=discord.Color.dark_purple()
    )

    if image_url:
        embed.set_image(url=image_url)

    return embed


class LaTeX(commands.Cog):
    """
    # Generates a LaTeX equation image using the CodeCogs API and displays it in an embed.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.session: aiohttp.ClientSession | None = None

    async def cog_load(self) -> None:
        self.session = aiohttp.ClientSession()

    async def cog_unload(self) -> None:
        if self.session:
            await self.session.close()

    @app_commands.command(description="Show the available LaTeX colors.")
    async def latex_colors(self, interaction: discord.Interaction) -> None:
        logger.info("%s used the /latex_colors command.", interaction.user.display_name)

        file = discord.File(
            Path.cwd().joinpath("src", "bot", "static", "images", "colors.png"),
            filename="colors.png",
        )
        embed = embed_info(
            "LaTeX Colors",
            "The following colors are available:",
            "attachment://colors.png",
        )
        await interaction.response.send_message(file=file, embed=embed, ephemeral=True)

    async def latex_available(self, image_path: str) -> bool:
        """
        Check whether the CodeCogs JSON response reports a valid equation.
        """
        try:
            if not self.session:
                return False

            json_path = image_path.replace(
                "png.image?",
                "png.json?",
                1,
            )

            async with self.session.get(json_path) as response:
                if response.status != 200:
                    return False
                data = await response.json(content_type="text/json")

                return data["latex"]["valid"]

        except (aiohttp.ClientError, KeyError, TypeError, ValueError):
            logger.exception("Failed to validate LaTeX equation with CodeCogs")
            return False

    def normalize_color(self, value: str, default: str) -> str:
        normalized = value.strip().replace(" ", "").lower()
        return LATEX_COLORS.get(normalized, default)

    async def render(
        self, equation: str, bg_color: str, txt_color: str, dpi: int
    ) -> discord.Embed:
        # Check for valid user specified color for text and background.
        bg_color = self.normalize_color(bg_color, "Black")
        txt_color = self.normalize_color(txt_color, "White")

        if txt_color == bg_color:
            txt_color = "White" if bg_color == "Black" else "Black"

        # Handle necessary character replacements.
        character_replacements = {
            "\n": r"\n",
            "\r": r"\r",
            "\t": r"\t",
            "\x08": r"\b",
            "\x0c": r"\f",
            "\x0b": r"\v",
            "\x07": r"\a",
            "#": "&hash;",
            " ": "&space;",
        }
        for old, new in character_replacements.items():
            equation = equation.replace(old, new)

        dpi = max(200, min(dpi, 800))

        image_path = (
            rf"https://latex.codecogs.com/png.image?"
            rf"\dpi{{{dpi}}}"
            rf"\color{{{txt_color}}}"
            r"\setlength{\fboxsep}{6pt}"
            r"\setlength{\fboxrule}{0pt}"
            rf"\colorbox{{{bg_color}}}{{${equation}$}}"
        )

        return embed_info(
            "LaTeX",
            equation.replace("&space;", " "),
            image_path,
        )

    @app_commands.command()
    async def latex(
        self,
        interaction: discord.Interaction,
        equation: str,
        *,
        bg_color: str = "Black",
        txt_color: str = "White",
        dpi: int = 300,
    ) -> None:
        """
        Send a mathematical equation using LaTeX.

        Parameters
        ----------
        equation : LaTeX equation (do not include `$` delimiters).
        bg_color : Background color. See `/latex_colors` for available colors.
        txt_color : Text color. See `/latex_colors` for available colors.
        dpi : Image resolution in DPI (200–800).
        """
        logger.info("%s used the /latex command.", interaction.user.display_name)

        view = LatexView(
            self,
            interaction,
            equation,
            bg_color,
            txt_color,
            dpi,
        )

        await interaction.response.defer(ephemeral=True)

        embed, file = await view.render()

        await interaction.edit_original_response(
            embed=embed,
            attachments=[file] if file else [],
            view=view,
        )


async def setup(bot: commands.Bot) -> None:
    """
    Required.
    """
    await bot.add_cog(LaTeX(bot))
