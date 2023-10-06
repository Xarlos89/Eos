"""
__main__.py entrypoint for the bot.
"""
import os
import discord
from db.core.database import DB

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    db = DB(os.getenv('RETOOL_DB'))
    # db.synchronise(client)
    print(f'We have logged in as {client.user}')


if __name__ == "__main__":
    client.run(os.getenv('BOT_TOKEN'))
