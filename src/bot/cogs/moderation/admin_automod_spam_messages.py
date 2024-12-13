import logging
from datetime import datetime, timedelta

import discord.errors
from discord.ext import commands

from zorak.utilities.cog_helpers._embeds import (
    # TODO: Move embeds into functions here in the file.
    embed_spammer,  # pylint: disable=E0401
    embed_spammer_warn  # pylint: disable=E0401
)

logger = logging.getLogger(__name__)


class ModerationSpamMessages(commands.Cog):
    """
    A cog for detecting and moderating spam messages in Discord channels.

    This cog monitors user messages to identify repeated messages sent in quick succession.
    Upon detecting repeated messages, it takes moderation actions such as warning or
    quarantining the user and deleting spam messages.
    """

    def __init__(self, bot):
        """
        Initializes the cog with the bot instance.

        Args:
            bot (commands.Bot): The bot instance to which this cog is added.
        """
        self.bot = bot
        self.records = {}
        self.warn_message = 'Hello there!'

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Listens for incoming messages and checks for repeated content.

        Args:
            message (discord.Message): The message object representing the user's message.
        """
        if message.author.bot or isinstance(message.channel, discord.DMChannel):
            return

        author_id = message.author.id
        content = message.content if message.content else message.attachments[0].filename

        record = self.records.get(author_id, {
            "last_message": None,
            "occurrence": 0,
            "messages": []
        })

        if record["last_message"] == content:
            record["occurrence"] += 1
            logger.debug("%s has sent a double message in %s", message.author.name, message.channel.name)

            record["messages"].append({
                "message_id": message.id,
                "channel_id": message.channel.id,
                "file_name": message.attachments[0].filename if not message.content else None,
                "file_url": message.attachments[0].url if not message.content else None
            })

            self.records[author_id] = record
            await self.handle_repeated_messages(message, record)
        else:
            self.records[author_id] = {
                "last_message": content,
                "occurrence": 1,
                "messages": [{
                    "message_id": message.id,
                    "channel_id": message.channel.id,
                    "file_name": message.attachments[0].filename if not message.content else None,
                    "file_url": message.attachments[0].url if not message.content else None
                }]
            }

    async def handle_repeated_messages(self, message, record):
        """
        Handles actions based on the number of repeated messages.

        Args:
            message (discord.Message): The message object triggering this action.
            record (dict): The user's message record containing repeated messages.
        """
        if record["occurrence"] == 2:
            await self.warn_user(message, record)

        # elif record["occurrence"] == 3:
        #     await self.quarantine_user(message, record)

    async def warn_user(self, message, record):
        """
        Warns the user for sending repeated messages.

        Args:
            message (discord.Message): The triggering message object.
            record (dict): The user's message record.
        """
        try:
            first_channel = await self.bot.fetch_channel(record["messages"][0]["channel_id"])
            second_channel = await self.bot.fetch_channel(record["messages"][1]["channel_id"])

            self.warn_message = await message.author.send(
                embed=embed_spammer_warn(first_channel, second_channel)
            )
            logger.debug("%s was sent a DM about their double message.", message.author.name)
        except discord.errors.Forbidden:
            first_channel = await self.bot.fetch_channel(record['messages'][0]['channel_id'])
            await message.reply(
                f"{message.author.mention}, Please do not post the same message in multiple channels.\n"
                f"You already posted this in {first_channel.mention}"
            )
        finally:
            await message.author.timeout(until=datetime.utcnow() + timedelta(seconds=15))
            logger.info("%s was timed out (2/3 messages)", message.author.name)

    # async def quarantine_user(self, message, record):
    #     # TODO: DATABASE ROLES.
    #     # We cannot yet set roles in the settings, so we cannot use commands that query roles.
    #     """
    #     Quarantines the user for sending three repeated messages and deletes the spam messages.
    #
    #     Args:
    #         message (discord.Message): The triggering message object.
    #         record (dict): The user's message record.
    #     """
    #     naughty_role = message.author.guild.get_role(self.bot.server_settings.user_roles["bad"]["naughty"])
    #     verified_role = message.author.guild.get_role(self.bot.server_settings.verified_role['verified'])
    #     quarantine_channel = await self.bot.fetch_channel(
    #         self.bot.server_settings.channels["moderation"]["quarantine_channel"]
    #     )
    #
    #     await message.author.timeout(until=datetime.utcnow() + timedelta(seconds=30))
    #     await message.author.remove_roles(verified_role)
    #     await message.author.add_roles(naughty_role)
    #
    #     await quarantine_channel.send(
    #         embed=embed_spammer(message.author, message.content, record["messages"][-1]["file_url"])
    #     )
    #
    #     for msg in record["messages"]:
    #         channel = await self.bot.fetch_channel(msg["channel_id"])
    #         msg_to_delete = await channel.fetch_message(msg["message_id"])
    #         await msg_to_delete.delete()
    #
    #     self.records[message.author.id] = {
    #         "last_message": message.content if message.content else message.attachments[0].filename,
    #         "occurrence": 1,
    #         "messages": [{
    #             "message_id": message.id,
    #             "channel_id": message.channel.id,
    #             "file_name": message.attachments[0].filename if not message.content else None,
    #             "file_url": message.attachments[0].url if not message.content else None
    #         }]
    #     }


def setup(bot):
    """
    Adds the ModerationSpamMessages cog to the bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog is added.
    """
    bot.add_cog(ModerationSpamMessages(bot))
