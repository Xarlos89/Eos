import os
from discord.ext import commands

def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

def is_moderator():
    async def predicate(ctx):
        return ctx.author.guild_permissions.ban_members
    return commands.check(predicate)

def is_master_guild():
    async def predicate(ctx):
        master_guild_id = int(os.getenv("MASTER_GUILD"))
        return ctx.guild and ctx.guild.id == master_guild_id
    return commands.check(predicate)
