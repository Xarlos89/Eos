import discord
from discord.ext import commands
from core.embeds import embed_info


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

       embed = discord.Embed(title="Available Settings")
       for setting in all_settings[0]["settings"]:
           embed.add_field(name=f"ID: {setting[0]}", value=f"{setting[1]}={setting[2]}", inline=False)

       await ctx.send(embed=embed)


    # TODO: Pick up here with CRUD operations

    # @commands.hybrid_command()
    # async def add_setting(self, ctx: commands.Context, name: str, value: str):
    #    """
    #    Add a new setting.

    #    >settings add name value
    #    """
    #    result = self.bot.api.add_new_setting(name, value)

    #    if result["status"] == "ok":
    #        await ctx.send(f"Successfully added setting: {result['message']}")
    #    else:
    #        await ctx.send(f"Failed to add setting: {result['message']}")

    @commands.hybrid_command()
    async def update_setting(self, ctx: commands.Context, setting_id: int, new_value: str):
       """
       Update an existing setting.

       >update_setting setting_id new_value
       """
       result = self.bot.api.update_existing_setting(setting_id, new_value)

       if result["status"] == "ok":
           await ctx.send(f"Successfully updated setting ID {setting_id}: {result['message']}")
       elif result["status"] == "not_found":
           await ctx.send(f"No setting found with ID {setting_id}. Please try again.")
       else:
           await ctx.send(f"Failed to update setting: {result['message']}")

    # @commands.hybrid_command()
    # async def delete_setting(self, ctx: commands.Context, setting_id: int):
    #    """
    #    Delete a setting.

    #    >settings delete setting_id
    #    """
    #    result = self.bot.api.delete_setting(setting_id)

    #    if result["status"] == "ok":
    #        await ctx.send(f"Successfully deleted setting ID {setting_id}: {result['message']}")
    #    elif result["status"] == "not_found":
    #        await ctx.send(f"No setting found with ID {setting_id}. Please try again.")
    #    else:
    #        await ctx.send(f"Failed to delete setting: {result['message']}")

async def setup(bot: commands.Bot) -> None:
   await bot.add_cog(Settings(bot))
