"""
Logging for message deletes
"""

import datetime
import logging
import os
from io import BytesIO

import discord
from discord.ext import commands

from src.bot.cogs import BaseCog

logger = logging.getLogger(__name__)


def embed_message_delete(some_member, some_message, some_moderator=None):
    """
    Embedding for user message deletion alerts.
    """
    embed = discord.Embed(
        title="<:red_circle:1043616578744357085> Deleted Message",
        description=f"{some_moderator.mention if some_moderator is not None else some_member.mention} deleted a message"
        f"\nIn {some_message.channel}\n"
        f"Message author: {some_member.mention}",
        color=discord.Color.red(),
        timestamp=datetime.datetime.now(datetime.timezone.utc),
    )

    embed.set_thumbnail(
        url=some_member.avatar if some_moderator is None else some_moderator.avatar
        # the person who DELETED the message
    )
    if len(some_message.content) > 1020:
        the_message = some_message.content[0:1020] + "..."
    else:
        the_message = some_message.content

    if not the_message:
        the_message = "*No text content*"
    embed.add_field(name="Message: ", value=the_message, inline=True)

    if some_message.attachments:
        embed.add_field(
            name="Attachments: ",
            value="\n".join(
                attachment.filename for attachment in some_message.attachments
            )[0:1020],
            inline=False,
        )

    return embed


class LoggingMessageDelete(BaseCog):
    """
    Simple listener to on_message_delete
    then checks the audit log for exact details
    """

    def __init__(self, bot):
        super().__init__(logger)

        self.bot = bot
        setting = self.bot.api.get_one_setting("3")  # Staff Channel ID
        if setting["status"] != "ok":
            raise RuntimeError("Failed to fetch staff channel setting from API.")
        self.staff_channel = setting["setting"]["value"]

        setting = self.bot.api.get_one_setting("1")  # Verification Channel ID
        if setting["status"] != "ok":
            raise RuntimeError("Failed to fetch verification channel setting from API.")
        self.verification_channel = setting["setting"]["value"]
        self.verification_command = f"{os.getenv('PREFIX')}verify"

        self.chat_log = self.bot.api.get_one_log_setting("3")  # chat_log
        if self.chat_log["status"] != "ok":
            raise RuntimeError("Failed to fetch chat log setting from API.")

    async def build_image_file(self, attachment: discord.Attachment) -> discord.File:
        """
        Return a File for the attachment, so it can be re-uploaded with the log embed.
        """
        data = await attachment.read()
        return discord.File(BytesIO(data), filename=attachment.filename)

    async def collect_image_files(self, message) -> list[discord.File]:
        """
        Re-download every image attachment on the deleted message.

        Discord purges the CDN copy shortly after a delete, so anything we
        fail to fetch is simply left out of the log rather than raising.
        """
        size_limit = message.guild.filesize_limit
        files = []
        for attachment in message.attachments:
            if not (
                attachment.content_type and attachment.content_type.startswith("image/")
            ):
                continue
            if attachment.size > size_limit:
                logger.debug(
                    f"Image attachment {attachment.filename} is too large to re-upload "
                    f"({attachment.size} > {size_limit}). Skipping."
                )
                continue
            logger.debug(
                f"Image attachment detected in deleted message, "
                f"{attachment.filename}:{attachment.url}"
            )
            try:
                files.append(await self.build_image_file(attachment))
            except discord.HTTPException as err:
                logger.warning(
                    f"Could not fetch deleted attachment {attachment.filename} -> {err}"
                )
        return files

    @commands.Cog.listener()
    async def on_message_delete(self, message) -> None:
        """
        If a mod deletes, take the audit log event. If a user deletes, handle it normally.
        """
        if message.guild is None:
            logger.debug(">> on_message_delete fired in DMs. Ignoring event.")
            return

        if message.guild.id != int(os.getenv("MASTER_GUILD", 0)):
            logger.warning(
                ">> on_message_delete fired, but not in master guild. Ignoring event."
            )
            return

        if message.channel.id == int(self.staff_channel):
            logger.debug("Message delete in staff channel was ignored.")
            return

        if message.channel.id == int(self.verification_channel) and (
            message.author.bot or message.content == self.verification_command
        ):
            logger.debug("Message from verification process was ignored.")
            return

        audit_log = [entry async for entry in message.guild.audit_logs(limit=1)][0]
        if self.chat_log["status"] == "ok":
            if self.chat_log["log_setting"]["value"] == "0":
                logger.debug(
                    f"log was triggered, but logging is disabled. API: {self.chat_log}"
                )
                return
            logs_channel = await self.bot.fetch_channel(
                self.chat_log["log_setting"]["value"]
            )

            image_files = await self.collect_image_files(message)

            if str(audit_log.action) == "AuditLogAction.message_delete":
                # Then a moderator deleted a message.
                embed = embed_message_delete(audit_log.target, message, audit_log.user)
                await logs_channel.send(embed=embed, files=image_files)

            else:
                # Otherwise, the author deleted it.
                username = message.author
                await logs_channel.send(
                    embed=embed_message_delete(username, message), files=image_files
                )
        else:
            logger.critical(f"API error. API response not ok. -> {self.chat_log}")


async def setup(bot: commands.Bot) -> None:
    """boink"""
    await bot.add_cog(LoggingMessageDelete(bot))
