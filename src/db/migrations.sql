BEGIN;

    -- Put all your migrations commands here.
        -- It is HIGHLY recommended to use EXISTS guards to not
    -- accidentally apply migrations more than once.

    INSERT INTO serversettings (name, value)
    SELECT 'Ticket Channel', '0'
    WHERE NOT EXISTS (
        SELECT * FROM serversettings
        WHERE name='Ticket Channel'
    );

    CREATE TABLE IF NOT EXISTS tickets (
        id SERIAL PRIMARY KEY,
        thread_id BIGINT NOT NULL UNIQUE,
        channel_id BIGINT NOT NULL,
        creator_id BIGINT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(50) DEFAULT 'open'
    );

COMMIT;
