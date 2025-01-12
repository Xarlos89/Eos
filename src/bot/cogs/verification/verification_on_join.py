"""
This is a handler that adds a Need Approval role and sends the user a message.
"""
import os
from asyncio import sleep
import logging
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class LoggingVerification(commands.Cog):
    """
    Handled with a role, and a message.
    the role limits the user to one channel, with a verify button.
    If the user does not push the button within one hour, they are auto-kicked.
    """

    def __init__(self, bot):
        self.bot = bot
        self.verification_channel = self.bot.api.get_one_setting('1')[0]['setting'][2]
        self.verification_log = self.bot.api.get_one_log_setting('4')[0]['logging'][2]
        self.join_log = self.bot.api.get_one_log_setting('4')[0]['logging'][2]
        self.verified_role = self.bot.api.get_one_role('6')[0]['roles'][2]
        self.naughty_role = self.bot.api.get_one_role('7')[0]['roles'][2]

    async def log_unverified_join(self, member, logging_channel):
        await logging_channel.send(f"<@{member.id}> joined, but has not verified.")

    async def send_welcome_message(self, guild, member):
        welcome_message = f"""
            Hi there, {member.mention}
            I'm Zorak, the moderator of {guild.name}.

            We are very happy that you have decided to join us.
            Before you are allowed to chat, you need to verify that you are NOT a bot.\n
            Dont worry... it's easy.
            Just go to {self.bot.get_channel(self.verification_log).mention}
            and use the **{os.getenv('PREFIX')}verify** command.

            After you do, all of {guild.name} is available to you. Have a great time :-)
            """
        # Send Welcome Message
        try:
            await member.send(welcome_message)
        except discord.errors.Forbidden as catch_dat_forbidden:
            logger.debug(f'{member.name} cannot be sent a DM.')

    async def kick_if_not_verified(self, member, time_to_kick, logging_channel):
        await sleep(time_to_kick)

        if all(x not in [role.id for role in member.roles] for x in (self.verified_role, self.naughty_role)):
            await logging_channel.send(
                f"{member.mention} did not verify after {int((time_to_kick / 3600))} hour/s, auto-removed.")
            await member.kick(reason="Did not verify.")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        logs_channel = await self.bot.fetch_channel(self.join_log)  # Join log

        await self.log_unverified_join(member, logs_channel)
        await self.send_welcome_message(guild, member)
        await self.kick_if_not_verified(member, 3600, logs_channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Keep verification clean again
        """
        if message.channel.id == int(self.verification_channel):
            if not message.author.bot and not message.author.guild_permissions.manage_roles:
                if "verify" in message.content:
                    # user might be doing it right
                    return

                channel_message = await message.channel.send(
                    f"You need to use the **{os.getenv('PREFIX')}verify** command.")

                await message.delete()
                logs_channel = await self.bot.fetch_channel(self.verification_log)
                await logs_channel.send(
                    f"{message.author} is failing at life in {self.bot.get_channel(self.verification_log).mention}")

                if channel_message:
                    await sleep(10)  # wait 10 seconds, and then we delete the message in the channel

                    async for msg in message.channel.history(limit=5):
                        if msg.author.bot:
                            await msg.delete()
                            break  # only delete 1


async def setup(bot: commands.Bot) -> None:
    """boink"""
    await bot.add_cog(LoggingVerification(bot))
