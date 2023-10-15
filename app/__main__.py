"""
__main__.py entrypoint for the bot.
"""
import os
import discord

from Eos.app.db.database import DB

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    db = DB(os.getenv('RETOOL_DB'), client)
    db.sync(guilds=False, channels=False, roles=False, members=False, settings=True)
    print(f'We have logged in as {client.user}')


if __name__ == "__main__":
    client.run(os.getenv('BOT_TOKEN'))
