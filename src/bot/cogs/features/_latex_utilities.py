from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from .latex import LaTeX

logger = logging.getLogger(__name__)


class LatexEditModal(discord.ui.Modal, title="Edit LaTeX"):
    equation = discord.ui.TextInput(
        label="LaTeX equation",
        style=discord.TextStyle.paragraph,
        required=True,
    )
    text_color = discord.ui.TextInput(label="Text color", required=False)
    bg_color = discord.ui.TextInput(label="Background color", required=False)
    dpi = discord.ui.TextInput(label="DPI", required=False)

    def __init__(self, view: "LatexView"):
        super().__init__()

        self.view = view

        self.equation.default = view.equation
        self.text_color.default = view.text_color
        self.bg_color.default = view.bg_color
        self.dpi.default = str(view.dpi)

    async def on_submit(self, interaction: discord.Interaction):
        self.view.equation = self.equation.value

        if self.text_color.value:
            self.view.text_color = self.text_color.value

        if self.bg_color.value:
            self.view.bg_color = self.bg_color.value

        if self.dpi.value:
            try:
                self.view.dpi = int(self.dpi.value)
            except ValueError:
                logger.exception(
                    "%s input a non-number value for DIP in the /latex command.",
                    interaction.user.display_name,
                )

        await interaction.response.defer(ephemeral=True)

        embed, file = await self.view.render()

        await interaction.edit_original_response(
            embed=embed,
            attachments=[file] if file else [],
            view=self.view,
        )


class LatexView(discord.ui.View):
    def __init__(
        self,
        latex: LaTeX,
        interaction: discord.Interaction,
        equation: str,
        bg_color: str,
        text_color: str,
        dpi: int,
    ):
        super().__init__(timeout=300)

        self.latex = latex
        self.interaction = interaction
        self.equation = equation
        self.bg_color = bg_color
        self.text_color = text_color
        self.dpi = dpi

    async def render(self) -> tuple[discord.Embed, discord.File | None]:
        embed = await self.latex.render(
            self.equation,
            self.bg_color,
            self.text_color,
            self.dpi,
        )

        if embed.image.url and await self.latex.latex_available(embed.image.url):
            return embed, None

        invalid = discord.File(
            Path.cwd().joinpath("src", "bot", "static", "images", "invalid.png"),
            filename="invalid.png",
        )
        embed.set_image(url="attachment://invalid.png")
        return embed, invalid

    @discord.ui.button(label="Edit", emoji="✏️", style=discord.ButtonStyle.primary)
    async def edit(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await interaction.response.send_modal(LatexEditModal(self))

    @discord.ui.button(label="Send", emoji="✅", style=discord.ButtonStyle.success)
    async def publish(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        embed = await self.latex.render(
            self.equation,
            self.bg_color,
            self.text_color,
            self.dpi,
        )

        if embed.image.url is None or not await self.latex.latex_available(
            embed.image.url
        ):
            await interaction.followup.send(
                content="Failed to display the LaTeX equation.",
                ephemeral=True,
            )
            return

        channel = interaction.channel

        if isinstance(channel, (discord.TextChannel, discord.Thread)):
            await channel.send(
                content=interaction.user.mention,
                embed=embed,
            )

        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True

        await self.interaction.edit_original_response(view=self)
