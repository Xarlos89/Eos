"""
__main__.py entrypoint for the bot.
"""
import os
import discord

from Eos.app.db.database import DB
from logger import log


client = discord.Client(intents=discord.Intents.all())


@client.event
async def before_identify_hook(shard_id, initial):
    if initial:
        log.info('Connecting to DB')
        # db = DB(os.getenv('RETOOL_DB'))
        log.info('Connection Success')

@client.event
async def on_ready():
    client.THROW_EXCEPTION
    # db.sync(client)
    log.info(f'We have logged in as {client.user}')

@client.event
async def on_error(event, *args, **kwargs):
    log.critical(event)




if __name__ == "__main__":
    client.run(os.getenv('BOT_TOKEN'))
