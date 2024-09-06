# Eos
A Discord.py bot, utilizing docker.

Commands and paths in this repo will be in Unix format.

# TL:DR
To run this bot, you will need Docker Compose.
1. `cd src/ && cp .env.EXAMPLE .env`
2. Replace "YOUR_DISCORD_BOT_TOKEN_HERE" with your Discord Bot token.
3. `docker compose up -d`
4. The bot should come online. You can use the `>hc` command to run a healthcheck on the system.

# Postgres Database
Currently using Postgres 16, the Postgres db will create a folder called postgres data at `/src/db/postgres-data/`
Do not delete this folder if you want the data in it to persist!

Otherwise, to reset the db run `sudo rm -r /src/db/postgres-db/`

The init script at/src/db/init.sql runs on the initial startup

# Flask API
The flask API is located at /src/api/
It should run on `http://127.0.0.1:5000` unless you've tampered with the .env settings for flask.

The functions that connect the API to the database are at `/src/api/core/db_helper.py` and serve as an abstraction over the psycopg functions.

# Discord.py Bot
The Bot is running using Discord.py, and cogged commands.
You may also run the bot manually for debugging using `python main.py` if your Token is in the .env
or by using `python main.py` is no .env is present
cogs are located at `/src/bot/cogs/*/`, and are seperated by their purpose.

The functions that connect the bot to the API are at `/src/bot/core/api_helper.py` and serve as an abstraction over the requests happening in the background.
There is also a `/src/bot/core/embeds.py`, however I might choose to depricate that in the future.
