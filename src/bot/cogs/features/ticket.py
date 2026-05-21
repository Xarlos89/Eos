"""
This cog allows us to create tickets.
"""
import logging

import discord
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger(__name__)

class TicketReasonModal(discord.ui.Modal, title="Create Ticket"):
    """
    This modal appears when the user selects a ticket type.
    It allows them to provide a reason or description for the ticket.
    """
    
    description = discord.ui.TextInput(
        label="Please describe The Issue...", 
        style=discord.TextStyle.short, 
        required=True, 
        max_length=1000
        )


    
    def __init__(self, bot, selected_option: str):
        super().__init__()
        self.bot = bot
        self.selected_option = selected_option

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        channel = self.bot.api.get_one_setting('5')
        staff_role = self.bot.api.get_one_role('3')
        staff_role = staff_role if staff_role['status'] == 'ok' else None
        
        if channel is None or channel['setting'][2] == "0":
            logger.warning("Ticket Channel not set in db. Cannot create ticket.")
            await interaction.response.send_message("Sorry, the ticket system is not set up yet. Please contact the staff directly.", ephemeral=True)
            return
        else:
            channel = guild.get_channel(int(channel['setting'][2])) # type: ignore

        option = self.selected_option if self.selected_option else "None Selected"

        thread_name = f"{option}-{interaction.user.name}".lower().replace(" ", "-")

        
        thread = await channel.create_thread( # type: ignore
            name=thread_name,
            type=discord.ChannelType.private_thread,
            invitable=False 
            ) 
        await thread.add_user(interaction.user) # type: ignore
        
        await thread.send(
            f'<@&{staff_role}> -- {interaction.user.mention} has created a ticket\n'
            f'Type: {option}\n'
            f'{self.description.value}'
            f'\n\n please provide any additional information here and our staff will assist you as soon as possible.'
        )
        
        self.bot.api.create_ticket(interaction.user.id, thread.id, option, self.description.value)
        
        await interaction.followup.send(f"Your ticket has been created! {thread.jump_url}", ephemeral=True)
        
class TicketDropdown(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot

        options = [
            discord.SelectOption(label="Moderation"),
            discord.SelectOption(label="Support"),
            discord.SelectOption(label="Proposition"),
            discord.SelectOption(label="Request"),
        ]

        super().__init__(
            placeholder="Select ticket type",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(
            TicketReasonModal(self.bot, self.values[0])
        )
        

class TicketView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=100)  # View will timeout after 1.5 minutes
        self.bot = bot
        self.add_item(TicketDropdown(bot))

    

class AddTicketModal(commands.Cog):
    """
    This is the slash command that sends our UI element.
    """

    def __init__(self, bot):
        self.bot = bot
        
        ticket_channel = self.bot.api.get_one_setting('5')
        
        
        if ticket_channel is None or ticket_channel['setting'][2] == "0":
            logger.warning("Ticket Channel not set in db. Ticket commands will not work until this is set.")
            raise RuntimeError("Ticket Channel not set in db. Ticket commands will not work until this is set.")
        else:
            self.ticket_channel = ticket_channel['setting'][2]
                
    @app_commands.command(description="Make a ticket and contact the Staff.")
    async def ticket(self, interaction: discord.Interaction):
        
        """
        A simple command with a view.
        """       
        logger.info("%s used the %s command.", interaction.user.name, interaction.command.name) # type: ignore
        
        await interaction.response.send_message("creating ticket...", view=TicketView(self.bot), ephemeral=True)

    

async def setup(bot: commands.Bot) -> None:
    """boink"""
    await bot.add_cog(AddTicketModal(bot))
