BEGIN;

    -- Put all your migrations commands here

    INSERT INTO serversettings (name, value)
    VALUES ('Server Announcement Channel', '0');

    INSERT INTO roles (name, value)
    VALUES ('Yapper', '0');

    ALTER TABLE users ADD COLUMN monthly_points int NOT NULL DEFAULT 0;

    CREATE TABLE IF NOT EXISTS parameters (
        parameter_name VARCHAR(255) NOT NULL,
        parameter_value VARCHAR(255)
    );
    INSERT INTO parameters (parameter_name, parameter_value)
    VALUES ('monthly_yapper', '0');

COMMIT;
