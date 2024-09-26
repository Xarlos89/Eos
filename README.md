# Eos
A Discord.py bot, utilizing docker.

Commands and paths in this repo will be in Unix format.

---
# TL:DR
To run this bot, you will need Docker Compose.
1. `cd src/ && cp .env.EXAMPLE .env`
2. Replace "YOUR_DISCORD_BOT_TOKEN_HERE" with your Discord Bot token.
3. `docker compose up -d`
4. The bot should come online. You can use the `>hc` command to run a healthcheck on the system.
---
# Infrastructure
### Postgres Database
Currently using Postgres 16, the Postgres db will create a folder called postgres data at `/src/db/postgres-data/`
Do not delete this folder if you want the data in it to persist!

Otherwise, to reset the db run `sudo rm -r /src/db/postgres-db/`

The init script at/src/db/init.sql runs on the initial startup

###  Flask API
The flask API is located at /src/api/
It should run on `http://127.0.0.1:5000` unless you've tampered with the .env settings for flask.

The functions that connect the API to the database are at `/src/api/core/db_helper.py` and serve as an abstraction over the psycopg functions.

### Discord.py Bot
The Bot is running using Discord.py, and cogged commands.
You may also run the bot manually for debugging using `python main.py` if your Token is in the .env
or by using `python main.py` is no .env is present
cogs are located at `/src/bot/cogs/*/`, and are seperated by their purpose.

The functions that connect the bot to the API are at `/src/bot/core/api_helper.py` and serve as an abstraction over the requests happening in the background.
There is also a `/src/bot/core/embeds.py`, however I might choose to depricate that in the future.

---
# Commands
## Points

### 1. `sync_users`
- **Description**: Synchronizes all guild members with the points database. Members who are already present in the database are skipped.
- **Arguments**: None.
- **Usage**: `>sync_users`
- **Output**: An embedded message showing how many users were added to the points table.



### 2. `get_points`
- **Description**: Retrieves and displays the points of a specific guild member.
- **Arguments**:
  - `user`: A mention or reference to a Discord member.
- **Usage**: `>get_points @user`
- **Output**: An embedded message displaying the mentioned user's current points.


### 3. `update_points`
- **Description**: Updates the points of a specific user by adding or subtracting a specified amount.
- **Arguments**:
  - `user`: A mention or reference to a Discord user.
  - `amount`: The number of points to add (positive) or subtract (negative).
- **Usage**: 
  - To add points: `>update_points @user 100`
  - To remove points: `>update_points @user -50`
- **Output**: An embedded message confirming the amount of points added or removed from the user.


### 4. `top_10`
- **Description**: Fetches and displays the top 10 users with the most points in the guild.
- **Arguments**: None.
- **Usage**: `>top_10`
- **Output**: An embedded message showing the top 10 users and their respective points.




