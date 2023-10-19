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
        # db = DB(os.getenv('RETOOL_DB'))
        database_check = DB.get_all_tables_in_db()
        if database_check:
            for table in database_check:
                log.info(f"- Successfully loaded {table}")


@client.event
async def on_ready():
    # db.sync(client)
    log.info(f'{client.user} is ready for commands.')


if __name__ == "__main__":
    client.run(os.getenv('BOT_TOKEN'))
