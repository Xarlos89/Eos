-- Drop existing database if it exists
DROP DATABASE IF EXISTS eos;

-- Create the database
CREATE DATABASE eos;

-- Rest of your initialization script...

-- Example: Creating tables
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
ALTER TABLE users ADD CONSTRAINT unique_discord_id UNIQUE (discord_id);
