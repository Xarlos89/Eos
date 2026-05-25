# Eos

A full-featured Discord bot built with Discord.py, designed to manage guild members, track points, and maintain customizable settings. The entire application runs within Docker containers for easy deployment and isolation.

**Note:** Commands and paths throughout this documentation use Unix/Linux format.

---

## Structure

Eos combines three main components working together:

- **Discord.py Bot** – Handles Discord interactions, commands, and real-time member management
- **Flask REST API** – Manages data operations and serves as the bridge between the bot and database
- **PostgreSQL Database** – Stores member data, points, and guild settings

This modular architecture makes it easy to extend functionality and debug individual components.

---

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system
- A Discord bot token (create one on the [Discord Developer Portal](https://discord.com/developers/applications))
- Basic familiarity with the command line

### Installation

1. **Clone the repository and navigate into it:**
   ```bash
   git clone https://github.com/Xarlos89/Eos.git
   cd Eos
   ```

2. **Set up your environment:**
   ```bash
   cd src
   cp .env.EXAMPLE .env
   ```

3. **Configure the `.env` file:**
   Open `.env` in your editor and update:
   - Replace `YOUR_DISCORD_BOT_TOKEN_HERE` with your Discord bot token
   - Set `MASTER_GUILD` to your guild's ID (the main server where the bot will operate)

4. **Start the bot:**
   ```bash
   docker compose up -d
   ```

5. **Verify everything is running:**
   ```
   >hc
   ```
   This runs a healthcheck command and confirms all services are operational.

### Troubleshooting Port Conflicts

If you already have PostgreSQL running locally, you'll likely hit a port conflict. Fix it by:

1. Editing `.env` and changing `POSTGRES_PORT` to an available port (usually `5433`)
2. Rebuild the containers:
   ```bash
   docker compose up -d --build
   ```

---

## Architecture

### PostgreSQL Database

- **Version:** 17.5
- **Default port:** Specified in `.env` (usually `5432`)
- **Data location:** `/src/db/postgres-data/`
  - **Important:** Don't delete this folder if you want to keep your data

**Resetting the database:**
```bash
sudo rm -r /src/db/postgres-data/
```

**Initialization:** The `init.sql` script at `/src/db/init.sql` runs automatically on first startup to set up tables and schemas.

### Flask API

- **Location:** `/src/api/`
- **Default URL:** `http://127.0.0.1:5000`
- **Database abstraction layer:** `/src/api/core/db_helper.py` – wraps psycopg functions for cleaner database queries

**Testing the API:**
A Postman collection is included in the `.postman/` directory for local testing and development.

### Discord.py Bot

- **Location:** `/src/bot/`
- **Command structure:** Organized by cogs in `/src/bot/cogs/` – each cog handles a specific category of commands
- **API integration:** `/src/bot/core/api_helper.py` – abstracts API calls and handles communication with the Flask backend
- **Embeds:** `/src/bot/core/embeds.py` – shared formatting for Discord embed messages (may be refactored in future versions)

**Manual testing:**
You can run the bot locally without Docker for debugging:
```bash
python main.py
```
Note: Many bot features depend on the full Docker stack, so this is mainly for testing individual functions.

---

## Commands

### Points Management

#### `sync_users`
Synchronizes all current guild members with the points database. Existing members are skipped, so it's safe to run multiple times.

- **Usage:** `>sync_users`
- **Output:** Embedded message showing how many users were added

#### `get_points`
Look up the current points for any guild member.

- **Usage:** `>get_points @user`
- **Output:** Embedded message displaying the user's points

#### `update_points`
Manually adjust a user's points (add or remove).

- **Usage:**
  - Add points: `>update_points @user 100`
  - Remove points: `>update_points @user -50`
- **Output:** Confirmation message with the updated total

#### `top_10`
Display the top 10 members by points.

- **Usage:** `>top_10`
- **Output:** Leaderboard-style embedded message

### Settings Management

#### `settings`
View all current guild settings.

- **Usage:** `>settings`
- **Output:** Embedded message with all active settings

#### `update_settings`
Interactively modify guild settings through a guided menu system.

- **Usage:** `>update_settings`
- **Interaction:** Follow the prompts to select which settings to change and enter new values

---

## Project Structure

```
Eos/
├── src/
│   ├── bot/                    # Discord bot code
│   │   ├── cogs/              # Organized command groups
│   │   ├── core/
│   │   │   ├── api_helper.py  # Bot↔API communication
│   │   │   └── embeds.py      # Message formatting
│   │   └── main.py            # Bot entry point
│   ├── api/                    # Flask REST API
│   │   ├── core/
│   │   │   └── db_helper.py   # Database abstraction
│   │   └── app.py             # API entry point
│   ├── db/
│   │   ├── init.sql           # Database initialization
│   │   └── postgres-data/     # Data storage (do not delete)
│   └── .env                   # Environment configuration
├── .postman/                   # Postman API collection
└── docker-compose.yml         # Container orchestration
```

---

## Development

### Adding New Commands

1. Create a new cog file in `/src/bot/cogs/`
2. Import the Discord.py Cog class and define your commands
3. Register the cog in the bot's main initialization

### Extending the API

1. Add new routes to `/src/api/`
2. Use `db_helper.py` for database operations
3. Test with the included Postman collection

### Database Changes

Modify `/src/db/init.sql` for schema changes. If starting fresh, the updated schema will apply on next startup. For existing databases, apply migrations manually or reset using the command above.

---

## Troubleshooting

**Bot isn't coming online:**
- Verify your Discord token is correct in `.env`
- Check that all Docker containers are running: `docker ps`
- Review logs: `docker compose logs bot`

**API connection errors:**
- Ensure Flask is running: `docker compose logs api`
- Verify the database is initialized: `docker compose logs db`

**Database issues:**
- Check PostgreSQL logs: `docker compose logs db`
- Verify the `.env` port matches your setup

---

## Future Improvements

- Make the bot startup independent from other services
- Refactor and potentially deprecate `embeds.py` for a cleaner message handling system
- Expand command set based on community feedback

---

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Feel free to open issues and pull requests.

---

**Created with ❤️ – Happy coding!**
