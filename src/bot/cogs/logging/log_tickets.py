import logging
import discord
from discord.ext import commands
from datetime import datetime

logger = logging.getLogger(__name__)


def embed_ticket_create(user, ticket_name):
    """
    Embed for creation of a new ticket.

    :param user: discord.Member.name
        - The user that created the ticket
    :param ticket_name: discord.Channel.id
        - The ID of the channel which was created
    """
    embed = discord.Embed(
        title=f'{str(user)} opened a ticket.',
        description=f"Ticket: {ticket_name}",
        color=discord.Color.green(),
        timestamp=datetime.utcnow(),
    )

    return embed


def embed_ticket_update(user, ticket_name):
    """
    Embed for update of a new ticket.

    :param user: discord.Member.name
        - The user that updated the ticket
    :param ticket_name: discord.Channel.id
        - The ID of the channel which was updated
    """
    embed = discord.Embed(
        title=f'{str(user)} updated a ticket.',
        description=f'Ticket: <#{ticket_name}>',
        color=discord.Color.green(),
        timestamp=datetime.utcnow(),
    )

    return embed


def embed_ticket_delete(user, ticket_name):
    """
    Embed for deletion of a new ticket.

    :param user: discord.Member.name
        - The user that deleted the ticket
    :param ticket_name: discord.Channel.id
        - The ID of the channel which was deleted
    """
    embed = discord.Embed(
        title=f'{str(user)} deleted a ticket.',
        description=f'Ticket: <#{ticket_name}>',
        color=discord.Color.red(),
        timestamp=datetime.utcnow(),
    )

    return embed


def embed_ticket_remove(user, ticket_name):
    """
    Embed for removal of a new ticket.

    :param user: discord.Member.name
        - The user that removed the ticket
    :param ticket_name: discord.Channel.id
        - The ID of the channel which was removed
    """
    embed = discord.Embed(
        title=f'{str(user)} removed a ticket.',
        description=f'Ticket: <#{ticket_name}>',
        color=discord.Color.red(),
        timestamp=datetime.utcnow(),
    )

    return embed


class LogTickets(commands.Cog):
    """
    Logs all form of thread creation and deletion when [ticket] is involved.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_create(self, thread) -> None:
        """
        When a thread is created

        :param thread: discord.Thread
            - The thread that was created.
        """
        audit_log = [entry async for entry in thread.guild.audit_logs(limit=1)][0]

        target = "AuditLogAction.thread_create"
        if str(audit_log.action) == target and str(audit_log.target).startswith("[Ticket]"):

            # TODO: Update this to pull form DB!
            # mod_log = await self.bot.fetch_channel(self.bot.server_settings.log_channel["mod_log"])
            embed = embed_ticket_create(audit_log.user, audit_log.target.mention)
            logger.info(f"A ticket was created by {audit_log.user}")
            # await mod_log.send(embed=embed)
            return

    @commands.Cog.listener()
    async def on_thread_update(self, before) -> None:
        """
        When a thread is updated, deleted or removed.

        :param thread: discord.Thread
            - The thread that was updated.
        """
        audit_log = [entry async for entry in before.guild.audit_logs(limit=1)][0]

        update = "AuditLogAction.thread_update"
        delete = "AuditLogAction.thread_delete"
        remove = "AuditLogAction.thread_remove"

        if str(audit_log.target).startswith("[Ticket]"):
            # TODO: Update this to pull form DB!
            # logs_channel = await self.bot.fetch_channel(self.bot.server_settings.log_channel["mod_log"])

            if str(audit_log.action) == update:
                embed = embed_ticket_update(audit_log.user, before.id)
                logger.info(f"{audit_log.user} updated a ticket.")
                #await logs_channel.send(embed=embed)
                return

            if str(audit_log.action) == delete:
                logger.info(f"{audit_log.user} deleted a ticket.")
                embed = embed_ticket_delete(audit_log.user, before.id)
                #await logs_channel.send(embed=embed)
                return

            if str(audit_log.action) == remove:
                logger.info(f"{audit_log.user} removed a ticket.")
                embed = embed_ticket_remove(audit_log.user, before.id)
                #await logs_channel.send(embed=embed)
                return


async def setup(bot: commands.Bot) -> None:
    """
    Necessary for loading the cog into the bot instance.
    """
    await bot.add_cog(LogTickets(bot))
