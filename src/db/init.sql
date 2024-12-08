DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'eos') THEN
        CREATE DATABASE eos;
    END IF;
END $$;


-- Create settings table
CREATE TABLE IF NOT EXISTS settings (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    value VARCHAR(255)
);

INSERT INTO settings (name, value)
VALUES
    ('Verification Log', '0'),
    ('Join Log', '0'),
    ('Chat Log', '0'),
    ('User Log', '0'),
    ('Mod Log', '0'),
    ('Server Log', '0'),
    ('Error Log', '0');



-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    discord_id VARCHAR(255) NOT NULL,
    points int NOT NULL
);
ALTER TABLE users
 ADD CONSTRAINT unique_discord_id UNIQUE (discord_id);