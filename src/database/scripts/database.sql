
IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'zorak_db') THEN
    CREATE DATABASE eos_db;
END IF;

DO $$
    BEGIN
    ----------------------------------------------------------------
    -- GUILDS
    ----------------------------------------------------------------
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'settings') THEN
        -- Create the table
        CREATE TABLE settings (
            id SERIAL PRIMARY KEY,
            status BOOL,
            value VARCHAR(255) NULL
        );
    END IF;

END $$;