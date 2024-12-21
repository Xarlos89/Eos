import logging
from datetime import datetime
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


def sanitize_string(input_string):
    """
    Necessary because not all channel names
    have ASCII characters, and Discord dropdown values don't like non ASCII
    """

    return ''.join(char for char in input_string if ord(char) < 128)

async def is_admin(ctx) -> bool:
    """ Check if the context user has admin permissions"""
    return ctx.message.author.guild_permissions.administrator


class Settings(commands.Cog):
    """
    Settings is made up of a "view". (Docs: https://discordpy.readthedocs.io/en/stable/interactions/api.html?highlight=ui%20view#select)
    This view uses a DropdownView, which contains a "dropdown", that is made up of many "SelectOption" objects.
    """
    def __init__(self, bot: commands.Bot) -> None:
        """Initialization of the points Class"""
        self.bot = bot

    @commands.check(is_admin)
    @commands.hybrid_command()
    async def settings(self, ctx: commands.Context):
       """
       List all available settings.

       >settings
       """
       all_settings = self.bot.api.get_all_settings()

       if all_settings[0]["status"] != "ok":
           await ctx.send(f"Failed to retrieve settings: {all_settings['message']}")
           return

       embed = discord.Embed(title="-- Settings --",
                      description="Here, you can see the current settings for the server.",
                      colour=0x000000,
                      timestamp=datetime.now())
       for setting in all_settings[0]["settings"]:
           embed.add_field(name=f"-- {setting[1]}"
                           , value=f"{setting[2] if setting[2] != '0' else 'Off'}"
                           , inline=False)
       embed.set_footer(text=ctx.guild.name,
                        icon_url=ctx.guild.icon)

       await ctx.send(embed=embed)

    @commands.check(is_admin)
    @commands.hybrid_command()
    async def update_settings(self, ctx: commands.Context):
        """
        Produces a dropdown of all available settings to change.
        """
        # Make the database calls to get the current data.
        channel_settings = self.bot.api.get_log_settings()
        role_settings = self.bot.api.get_all_roles()

        # Pull the names out of the returned JSON
        logging_types = [item for item in channel_settings[0]['settings']]
        role_types = [role for role in role_settings[0]['roles']]

        # Get the names of the available channels and roles to map
        channels = [channel for channel in ctx.guild.text_channels if "log" in channel.name]
        roles = [role for role in reversed(ctx.guild.roles)][:24] # TODO: Find a way to handle more than 25 roles

        # Pass a tuple. Index 0 is the title, index 2 is the view
        # Relevant in the prompt callback.
        menu = [
            ((log[1], LoggingDropdownView(ctx, self.bot, channels, log)) for log in logging_types),
            ((role[1], RoleDropdownView(ctx, self.bot, roles, role)) for role in role_types)
        ]

        prompt = PromptDropdownView(menu)
        await ctx.send(f"# Eos settings.\nWhich settings would you like to change?", view=prompt)

class PromptDropdown(discord.ui.Select):
    """
    This class serves as a "Main Menu" for our settings.
    We can adjust the menu options in the "Options" list.
    The logic for handling which sub-menu to send off is done in the callback.
    """
    def __init__(self, main_menu: list[tuple]):
        self.main_menu = list(main_menu) if not isinstance(main_menu, list) else main_menu
        options = [
            discord.SelectOption(label='Logging', description='Edit the logging settings', emoji='➡️', value="logging"),
            discord.SelectOption(label='Roles', description='Edit the role settings', emoji='➡️', value="roles"),
        ]
        super().__init__(placeholder='Choose an option...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == 'logging':
            await interaction.response.send_message(
"""
# -- Logging Settings --
Please select the channel you would like the relevant logs to go to.
If you do not want logs for something, you can select the "Turn off logging" option. 
"""
            )
            for title, view in self.main_menu[0]:
                await interaction.channel.send(f"### **{title}**", view=view)

        if self.values[0] == 'roles':
            await interaction.response.send_message(
"""
# -- Role Settings --
Please select the server roles you'd like to configure for the positions available.
1. Owner - The owner of the server. This role has the highest permissions.
2. Admin - This role also has the highest permissions, but is assigned. 
3. Staff - This role is for moderators. Gives access to moderation commands.
4. Privileged - This role is for privileged users. Gives access to logging.
5. Ping - This role is for server notifications and pingable events. 
6. Verified - This role is for verification of users. Allows access to the server. (DANGEROUS!)
7. Quarantine - This role is for quarantining user until moderation action is taken. 
    
"""
            )
            for title, view in self.main_menu[1]:
                await interaction.channel.send(f"### **{title}**", view=view)
class PromptDropdownView(discord.ui.View):
    def __init__(self, logging_view):
        super().__init__()
        # Adds the dropdown to our view object.
        self.add_item(PromptDropdown(logging_view))


class LoggingDropdown(discord.ui.Select):
    def __init__(self, ctx: commands.Context, bot, channels: list, purpose: str):
        self.bot = bot
        self.guild = ctx.guild
        self.channels = channels
        self.dropdown_options = [
            discord.SelectOption(
                label="Turn off logging."
                , description="..."
                , emoji="🔴"
                # Special formatting that uses : as a delimiter.
                # Kind of abusing the "value" option with this.
                # See the callback
                , value=f"{purpose[0]}:{purpose[1]}:0")
        ]

        for guild_channel in self.channels:
            logging.debug(f'Length of dropdown options: {len(self.channels)}') # Maximum 25!
            self.dropdown_options.append(
                discord.SelectOption(
                    label=f"#{sanitize_string(guild_channel.name)}"
                    , description=guild_channel.topic if guild_channel.topic is not None else None
                    , emoji="➡️"
                    # Special formatting that uses : as a delimiter.
                    # Kind of abusing the "value" option with this.
                    # See the callback
                    , value=f"{purpose[0]}:{purpose[1]}:{guild_channel.id}"
                )
            )
            logger.debug(f"SelectOption value: {purpose}:{guild_channel.id}")

        super().__init__(placeholder="Select a channel.", min_values=1, max_values=1, options=self.dropdown_options)

    async def callback(self, interaction: discord.Interaction):
        # The special handling from above.
        # value[0] will be the Database ID of the channel
        # value[1] will be the name of the setting... i.e. "Chat Log"
        # value[2] will be the Discord ID of the channel
        value = self.values[0].split(":")
        self.bot.api.update_existing_setting(value[0], value[2])

        logger.info(f'The {value[1]} setting was changed to: {value[2]}')
        await interaction.response.send_message(
            f'The {value[1]} will log to <#{value[2]}>' if value[2]!="0" else f'The {value[1]} will not log anything.'
        )

class RoleDropdown(discord.ui.Select):
    def __init__(self, ctx: commands.Context, bot, roles: list, purpose: str):
        self.bot = bot
        self.guild = ctx.guild
        self.roles = roles
        self.dropdown_options = [
            discord.SelectOption(
                label="Disconnect role."
                , description=f"Disconnect the role from the {purpose[1]} position"
                , emoji="🔴"
                # Special formatting that uses : as a delimiter.
                # Kind of abusing the "value" option with this.
                # See the callback
                , value=f"{purpose[0]}:{purpose[1]}:0")
        ]

        for role in self.roles:
            logging.debug(f'Length of dropdown options: {len(self.roles)}') # Maximum 25!
            self.dropdown_options.append(
                discord.SelectOption(
                    label=f"{sanitize_string(role.name)}"
                    , description=None
                    , emoji="➡️"
                    # Special formatting that uses : as a delimiter.
                    # Kind of abusing the "value" option with this.
                    # See the callback
                    , value=f"{purpose[0]}:{purpose[1]}:{role.id}"
                )
            )
            logger.debug(f"SelectOption value: {purpose}:{role.id}")

        super().__init__(placeholder="Select a role.", min_values=1, max_values=1, options=self.dropdown_options)

    async def callback(self, interaction: discord.Interaction):
        # The special handling from above.
        # value[0] will be the Database ID of the role
        # value[1] will be the name of the role... i.e. "Owner"
        # value[2] will be the Discord ID of the role
        value = self.values[0].split(":")
        self.bot.api.update_existing_role(value[0], value[2])

        logger.info(f'The {value[1]} role was changed to: {value[2]}')
        await interaction.response.send_message(
            f'The {value[1]} role will be tied to <@&{value[2]}>' if value[2]!="0" else f'The {value[1]} role will not be linked to anything.'
        )

class LoggingDropdownView(discord.ui.View):
    def __init__(self, ctx: commands.Context, bot, channels: list, purpose: str):
        super().__init__()
        # Adds the dropdown to our view object.
        self.add_item(LoggingDropdown(ctx, bot, channels, purpose))

class RoleDropdownView(discord.ui.View):
    def __init__(self, ctx: commands.Context, bot, roles: list, purpose: str):
        super().__init__()
        # Adds the dropdown to our view object.
        self.add_item(RoleDropdown(ctx, bot, roles, purpose))


async def setup(bot: commands.Bot) -> None:
   await bot.add_cog(Settings(bot))
