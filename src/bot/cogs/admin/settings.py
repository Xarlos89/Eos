import logging
import discord
from discord.ext import commands
from core.embeds import embed_info

logger = logging.getLogger(__name__)

class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
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
    async def update_setting(self, ctx: commands.Context, setting_id: int, new_value: str = None):
       """
       Update an existing setting.
       """
       result = self.bot.api.update_existing_setting(setting_id, new_value)[0]
       if result["status"] == "ok":
           await ctx.send(f"Successfully updated setting ID {setting_id}: {result['message']}")
       elif result["status"] == "not_found":
           await ctx.send(f"No setting found with ID {setting_id}. Please try again.")
       else:
           await ctx.send(f"Failed to update setting: {result['message']}")


async def setup(bot: commands.Bot) -> None:
   await bot.add_cog(Settings(bot))
