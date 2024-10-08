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
    value TEXT NOT NULL
);

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    discord_id VARCHAR(255) NOT NULL,
    points int NOT NULL
);
ALTER TABLE users
 ADD CONSTRAINT unique_discord_id UNIQUE (discord_id);