import logging
import discord
from discord.ext import commands
from core.embeds import embed_info

logger = logging.getLogger(__name__)


def sanitize_string(input_string):
    # Necessary because not all channel names
    # have ASCII characters, and Discord dropdown values dont like non ASCII
    return ''.join(char for char in input_string if ord(char) < 128)


class Settings(commands.Cog):
    """
    Settings is made up of a "view". (Docs: https://discordpy.readthedocs.io/en/stable/interactions/api.html?highlight=ui%20view#select)
    This view uses a DropdownView, which contains a "dropdown", that is made up of many "SelectOption" objects.
    """
    def __init__(self, bot: commands.Bot) -> None:
        """Initialization of the points Class"""
        self.bot = bot

    @commands.hybrid_command()
    async def settings(self, ctx: commands.Context):
       """
       List all available settings.

       >settings list
       """
       all_settings = self.bot.api.get_all_settings()

       if all_settings[0]["status"] != "ok":
           await ctx.send(f"Failed to retrieve settings: {all_settings['message']}")
           return

       embed = discord.Embed(title="Settings")
       for setting in all_settings[0]["settings"]:
           embed.add_field(name=f"ID: {setting[0]}", value=f"{setting[1]}={setting[2]}", inline=False) #TODO: Ugly

       await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def update_setting(self, ctx: commands.Context):
        channel_settings = self.bot.api.get_log_settings()

        # Pull the names out of the returned JSON
        logging_types = [item[1] for item in channel_settings[0]['settings']]
        logger.debug(f"Log Channels: {logging_types}")

        # Get the names of the availible guild channels
        channels = [channel for channel in ctx.guild.text_channels if "log" in channel.name]

        # Throw that shit into a discord.View
        for log in logging_types:
            view = DropdownView(ctx, channels, log)
            await ctx.send(f"## **{log}**", view=view)

    # @commands.hybrid_command()
    # async def update_setting(self, ctx: commands.Context, setting_id: int, new_value: str = None):
    #    """
    #    Update an existing setting.
    #    """
    #    result = self.bot.api.update_existing_setting(setting_id, new_value)[0]
    #    if result["status"] == "ok":
    #        await ctx.send(f"Successfully updated setting ID {setting_id}: {result['message']}")
    #    elif result["status"] == "not_found":
    #        await ctx.send(f"No setting found with ID {setting_id}. Please try again.")
    #    else:
    #        await ctx.send(f"Failed to update setting: {result['message']}")

class Dropdown(discord.ui.Select):
    def __init__(self, ctx: commands.Context, channels: list, purpose: str):
        self.guild = ctx.guild
        self.channels = channels
        self.dropdown_options = []

        for guild_channel in self.channels:
            logging.debug(f'Length of dropdown options: {len(self.channels)}') # Maximum 25!
            self.dropdown_options.append(
                discord.SelectOption(
                    label=sanitize_string(guild_channel.name)
                    , description=guild_channel.topic if guild_channel.topic is not None else f'...'
                    # The value we send when a user selects something is
                    # ex: Server Log:12345643412312
                    # purpose and then channel ID
                    , value=f"{purpose}:{guild_channel.id}"
                )
            )
            logger.debug(f"SelectOption value: {purpose}:{guild_channel.id}")

        super().__init__(placeholder="Select a channel.", min_values=1, max_values=1, options=self.dropdown_options)

    async def callback(self, interaction: discord.Interaction):
        # TODO: This now needs to throw the new channel data back into the Database.
        value = self.values[0].split(":")
        logger.info(f'The {value[0]} setting was changed to: {value[1]}')
        await interaction.response.send_message(f'The {value[0]} will log to {value[1]}')

class DropdownView(discord.ui.View):
    def __init__(self, ctx: commands.Context, channels: list, purpose: str):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown(ctx, channels, purpose))



async def setup(bot: commands.Bot) -> None:
   await bot.add_cog(Settings(bot))
