DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'eos') THEN
        CREATE DATABASE eos;
    END IF;
END $$;

-- Create serversettings table
CREATE TABLE IF NOT EXISTS serversettings (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    value VARCHAR(255)
);

INSERT INTO serversettings (name, value)
VALUES
    ('Verification Channel', '0'),
    ('Quarantine Channel', '0'),
    ('Staff Channel', '0'),
    ('Bot Spam Channel', '0');


-- Create logging table
CREATE TABLE IF NOT EXISTS logging (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    value VARCHAR(255)
);

INSERT INTO logging (name, value)
VALUES
    ('Verification Log', '0'),
    ('Join Log', '0'),
    ('Chat Log', '0'),
    ('User Log', '0'),
    ('Mod Log', '0'),
    ('Server Log', '0'),
    ('Error Log', '0');

-- Create roles table
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    value VARCHAR(255)
);

INSERT INTO roles (name, value)
VALUES
    ('Owner', '0'),
    ('Admin', '0'),
    ('Staff', '0'),
    ('Privileged', '0'),
    ('Ping', '0'),
    ('Verified', '0'),
    ('Quarantine', '0');


-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    discord_id VARCHAR(255) NOT NULL,
    points int NOT NULL
);
ALTER TABLE users
 ADD CONSTRAINT unique_discord_id UNIQUE (discord_id);