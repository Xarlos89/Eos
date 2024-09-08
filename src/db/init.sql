DO $$
BEGIN
    ----------------------------------------------------------------
    -- Check if the database exists and create it if not
    ----------------------------------------------------------------
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'eos') THEN
        CREATE DATABASE eos;
    END IF;

    ----------------------------------------------------------------
    -- settings
    ----------------------------------------------------------------
    CREATE TABLE IF NOT EXISTS settings (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        value TEXT NOT NULL
    );

    ----------------------------------------------------------------
    -- points
    ----------------------------------------------------------------
    CREATE TABLE IF NOT EXISTS points (
        id SERIAL PRIMARY KEY,
        discord_id VARCHAR(255) NOT NULL,
        amount int NOT NULL
    );


END $$;
