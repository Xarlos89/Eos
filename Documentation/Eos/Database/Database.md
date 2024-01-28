## Postgres
The Postgres database is standard, with all the magic happening in the docker-compose.
The database folder at src/database/scripts is copied over to /docker-entrypoint-initdb.d in the docker container, which is run on startup of the container. 

The script itself has checks to not run the commands if the database and it's tables are present. 
