DO $$
BEGIN
    ----------------------------------------------------------------
    -- Check if the database exists and create it if not
    ----------------------------------------------------------------
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'postgres') THEN
        CREATE DATABASE postgres;
    END IF;

    ----------------------------------------------------------------
    -- settings
    ----------------------------------------------------------------
    IF
        NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'settings') THEN
            -- Create the table
            EXECUTE '
                CREATE TABLE settings (
                    id SERIAL PRIMARY KEY,
                    flag_1 BOOL NOT NULL,
                    flag_2 BOOL NOT NULL,
                    flag_3 BOOL NOT NULL,
                    flag_4 BOOL NOT NULL,
                    flag_5 BOOL NOT NULL,
                )';
    END IF;


END $$;
