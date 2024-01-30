import logging
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


async def is_admin(ctx) -> bool:
    return ctx.message.author.guild_permissions.administrator


class Admin_Settings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command()
    async def get_all_settings(self, ctx: commands.Context) -> None:
        logger.debug("get_settings command used.")
        await ctx.channel.send(self.bot.api.get_all_settings())

    @commands.hybrid_command()
    async def get_guild_settings(self, ctx: commands.Context, guild: discord.Guild) -> None:
        logger.debug("get_settings command used.")
        await ctx.channel.send(self.bot.api.get_settings_for_guild(guild.id))

    @commands.hybrid_command()
    @commands.check(is_admin)
    async def log_channel_settings(self, ctx: commands.Context):
        logs = ["User Join/Leave Log", "User Change Log", "Chat Log", "Moderation Log", "Server Change Log"]

        await ctx.send("# Logging Settings")
        for setting in logs:
            await ctx.send(f"### {setting}", view=LogChannelSelectMenu(self.bot, setting))

    @log_channel_settings.error
    async def log_channel_settings_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('Oie, you cant use that.')


class LogChannelSelectMenu(discord.ui.View):
    def __init__(self, bot, target, *, timeout=180):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.add_item(SelectChannels(self.bot, target))


class SelectChannels(discord.ui.ChannelSelect):
    def __init__(self, bot, label):
        super().__init__(
            placeholder=f"{label}"
            , channel_types=[discord.ChannelType.text, discord.ChannelType.private]
            , max_values=1
            , min_values=0
        )
        self.bot = bot
        self.label = label

    async def callback(self, interaction: discord.Interaction):
        channel_obj = self.values[0]
        logger.info(f"{interaction.user.name} set the {self.label} to #{channel_obj.name}")

        payload = {
            "target": self.label
            , "channel_id": channel_obj.id
            , "status": False if channel_obj is None else True
        }
        logger.info(payload)
        self.bot.api.update_settings(payload, interaction.guild_id)
        await interaction.response.send_message(content=f"{self.label} is set to: {channel_obj.mention}",
                                                ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin_Settings(bot))
