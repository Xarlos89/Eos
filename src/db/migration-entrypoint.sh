#!/bin/sh

set -e

until pg_isready -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DATABASE"; do
    sleep 1
done

if [ "$RUN_MIGRATIONS_BEFORE_STARTUP" = "true" ]; then
    echo "Server started, running migrations..."
    echo ""

    MIGRATION_FILE_PATH="migrations.sql"

    if [ ! -f "$MIGRATION_FILE_PATH" ]; then
        echo "Migration file not found, exiting."
        exit 1
    fi

    psql -h "$POSTGRES_HOST" \
        -U "$POSTGRES_USER" \
        -d "$POSTGRES_DATABASE" \
        -f "$MIGRATION_FILE_PATH"

    echo ""
    echo "Migrations ran successfully. Continuing normally."
else
    echo "No migrations to run. Continuing normally."
fi
