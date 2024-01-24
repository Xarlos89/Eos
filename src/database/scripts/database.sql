DO $$
BEGIN

    ----------------------------------------------------------------
    -- Check if the database exists and create it if not
    ----------------------------------------------------------------
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'eos_db') THEN
        CREATE DATABASE eos_db;
    END IF;

    ----------------------------------------------------------------
    -- settings
    ----------------------------------------------------------------
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'settings') THEN
        -- Create the table
        EXECUTE '
            CREATE TABLE settings (
                id SERIAL PRIMARY KEY,
                guild_id VARCHAR(255) NOT NULL,
                join_log varchar(255),
                chat_log varchar(255),
                mod_actions_log varchar(255),
                server_change_log varchar(255),
                bot_error_log varchar(255),
                status BOOL,
                value VARCHAR(255) NULL
            )';
    END IF;

END $$;
