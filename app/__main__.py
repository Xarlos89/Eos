"""
__main__.py entrypoint for the bot.
"""
import os
import discord
from logging import log

from Eos.app.db.database import DB


client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    db = DB(os.getenv('RETOOL_DB'))
    db.sync(client)
    log.info(f'We have logged in as {client.user}')


if __name__ == "__main__":
    client.run(os.getenv('BOT_TOKEN'))
