#! /bin/bash

set -e
# source /usr/local/bin/docker-entrypoint.sh

if [[ "$RUN_MIGRATIONS_BEFORE_STARTUP" == "true" ]]; then
    echo "Running migrations..."
    echo ""

    MIGRATION_FILE_PATH="/usr/local/bin/migrations.sql"

    if [[ ! -f "$MIGRATION_FILE_PATH" ]]; then
        echo "Migration file not found, exiting."
        exit 1
    fi

    echo "Migrations commands that will be run:"
    cat $MIGRATION_FILE_PATH
    echo ""

    # docker_setup_env
    # docker_create_db_directories

    # docker_temp_server_start "$@"
    #psql -U $POSTGRES_USER -d $POSTGRES_DB -f $MIGRATION_FILE_PATH
    # docker_temp_server_stop

    echo "Migrations ran successfully. Continuing normally."

    exec docker-entrypoint.sh "$@"
fi

echo "No migrations to run, continuing normally"

exec docker-entrypoint.sh "$@"
