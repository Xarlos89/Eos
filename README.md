# Eos

Eos is a Discord bot that utilizes modern technologies to be robust, scalable and deployable anywhere.

## Overview
The Bot communicates with a database via an API. All three of these moving parts are easily deployed using Docker.

#### The Bot
- The bot is written in Discord.py and features advanced logging, cogs, commands and more.

#### The API
- The Eos API is written in Flask, and uses blueprints to manage routes.

#### The Database
- the Eos Database is written in PostgresSQL, and is ready to handle anything that can be thrown at it. 


## Deployment
### ... in production
After filling out the information in your .env file, simply:
```bash
docker compose up -d
```

### ... in development
After filling out the information in your .env file, simply:
```bash
docker compose up -d
```
After making changes to code, build the service that you changed.
```bash
docker compose up -d --build api
# OR
docker compose up -d --build bot
# OR 
docker compose up -d --build db
# OR to rebuild everything
docker compose up -d --build
```
To inspect your logs run:
```bash
docker logs api
# OR
docker logs bot
# OR
docker logs db
```


## Releases, Versioning and the Changelog
We use release drafter to changelog and version the releases. 

Any PR into Prod will trigger a release.
- The Name of the PR into prod must start with 'major' or 'minor' otherwise it will be a patch release
  - Major = v1.x.x
  - Minor = vx.1.x
  - Patch = vx.x.1


Any PR with Github labels into Development will add an item to the changelog.

The label categorizes the entry in the changelog.

category: '🚀 Features'
- 'feature'
- 'enhancement'

category: '🐛 Bug Fixes'
- 'bugfix'
- 'patch'

category: '🧰 Maintenance'
- 'chore'
- 'cleanup'
- 'documentation'