"""
This cog allows us to create tickets.
"""
import logging

import discord
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger(__name__)

class TicketReasonModal(discord.ui.Modal, title="Create a Ticket"):
    """
    This modal appears when the user selects a ticket type.
    It allows them to provide a reason or description for the ticket.
    """
    description = discord.ui.TextInput(
        label="Please describe the issue or reason for the ticket. ", 
        style=discord.TextStyle.paragraph, 
        required=True, max_length=1000
        )

    def __init__(self, bot, ticket_type: str):
        super().__init__()
        self.ticket_type = ticket_type
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        channel = self.bot.api.get_one_setting('5')
        
        if channel is None or channel['setting'][2] == "0":
            logger.warning("Ticket Channel not set in db. Cannot create ticket.")
            await interaction.response.send_message("Sorry, the ticket system is not set up yet. Please contact the staff directly.", ephemeral=True)
            return
        else:
            channel = guild.get_channel(int(channel['setting'][2])) # type: ignore

        

        thread_name = f"{self.ticket_type}-{interaction.user.name}".lower().replace(" ", "-")

        
        thread = await channel.create_thread( # type: ignore
            name=thread_name,
            type=discord.ChannelType.private_thread,
            invitable=False
            ) 
        await thread.add_user(interaction.user) # type: ignore
        
        await thread.send(
            f'<@&{self.staff_role}> -- {interaction.user.mention} has created a ticket\n'
            f'Type: {self.ticket_type}\n'
            f'{self.description.value}'
            f'\n\n please provide any additional information here and our staff will assist you as soon as possible.'
        )
        
        self.bot.db.create_ticket(interaction.user.id, thread.id, self.ticket_type, self.description.value)
        
        await interaction.response.send_message(f"Your ticket has been created! {thread.jump_url}", ephemeral=True)
        

class TicketDropdown(discord.ui.Select):
    """
    This is the dropdown that appears when the user clicks 
    the button to create a ticket. It allows them to select the 
    type of ticket they want to create.
    """
    def __init__(self, bot):
        self.bot = bot
        
        options = [
            discord.SelectOption(
                label="Moderation",
                description="Report users or moderation issues"
            ),
            discord.SelectOption(
                label="Support",
                description="General support ticket"
            ),
            discord.SelectOption(
                label="Proposition",
                description="Suggest an idea or partnership"
            ),
            discord.SelectOption(
                label="Request",
                description="Request something from staff"
            )
        ]
        
        super().__init__(
            placeholder="Please select a ticket type",
            min_values=1,
            max_values=1,
            options=options)
    
    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        await interaction.response.send_modal(TicketReasonModal(self.bot, selected))

        


class TicketView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    

class AddTicketModal(commands.Cog):
    """
    This is the slash command that sends our UI element.
    """

    def __init__(self, bot):
        self.bot = bot
        
        ticket_channel = self.bot.api.get_one_setting('5')
        
        staff_role = self.bot.api.get_one_role('3')
        
        self.staff_role = staff_role if staff_role['status'] == 'ok' else None
        
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
        await interaction.response.defer()
        
        await interaction.followup.send(
            "Do you need help, or do you have a question for the Staff?",
            view=TicketView(self.bot),
            ephemeral=True,
        )


async def setup(bot: commands.Bot) -> None:
    """boink"""
    await bot.add_cog(AddTicketModal(bot))
