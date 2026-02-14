import os
import logging
import psycopg
from psycopg import OperationalError

logger = logging.getLogger(__name__)


class DB:
    def __init__(self):
        self.conn = psycopg.connect(
            dbname=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST')
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    ##################
    ## Healthchecks ##
    ##################
    def database_health_check(self):
        logger.debug("API attempting to contact DB for healthcheck...")
        try:
            self.cursor.execute("SELECT 1")
            result = self.cursor.fetchone()
            if result:
                return {"status": "ok"}

        except OperationalError as err:
            logger.critical(f"DB Healthcheck - 500 - {err}")
            self.conn.close()
            return {"status": "unhealthy", "error": {err}}

    ##################
    ##   logging   ##
    ##################
    def get_log_setting(self, setting_id):
        logger.debug("API attempting to contact DB for get_log_setting...")
        try:
            self.cursor.execute("SELECT * FROM logging where id = %s", (setting_id,))
            result = self.cursor.fetchone()
            return {"status": "ok", "logging": result}
        except OperationalError as err:
            logger.error(f"Error fetching logging: {err}")
            return {"status": "error", "message": str(err)}

    def get_log_settings(self):
        logger.debug("API attempting to contact DB for get_log_settings...")
        try:
            self.cursor.execute("SELECT * FROM logging") # case sensitive
            result = self.cursor.fetchall()
            return {"status": "ok", "logging": result}
        except OperationalError as err:
            logger.error(f"Error fetching logging: {err}")
            return {"status": "error", "message": str(err)}

    def get_logging(self):
        logger.debug("API attempting to contact DB for get_logging...")
        try:
            self.cursor.execute("SELECT * FROM logging")
            result = self.cursor.fetchall()
            return {"status": "ok", "logging": result}
        except OperationalError as err:
            logger.error(f"Error fetching logging: {err}")
            return {"status": "error", "message": str(err)}

    def update_logging(self, log_id, value):
        logger.debug(f"API attempting to contact DB for update_logging with log ID:{log_id} - Value:{value}")
        try:
            self.cursor.execute("UPDATE logging SET value = %s WHERE id = %s", (value, log_id))
            return {"status": "ok", "message": "Log setting updated successfully"}
        except OperationalError as err:
            logger.error(f"Error updating log setting: {err}")
            return {"status": "error", "message": str(err)}

    def add_log_setting(self, name, value):
        logger.debug(f"API attempting to contact DB for add_log with name:{name} - Value:{value}")
        try:
            self.cursor.execute("INSERT INTO logging (name, value) VALUES (%s, %s)", (name, value))
            return {"status": "ok", "message": "New log setting added successfully"}
        except OperationalError as err:
            logger.error(f"Error adding new log setting: {err}")
            return {"status": "error", "message": str(err)}

    def delete_log_setting(self, log_id):
        logger.debug(f"API attempting to contact DB for delete_log with log_ID:{log_id}")
        try:
            self.cursor.execute("DELETE FROM logging WHERE id = %s", (log_id,))
            return {"status": "ok", "message": f"Log with ID {log_id} deleted successfully"}
        except OperationalError as err:
            logger.error(f"Error deleting log setting: {err}")
            return {"status": "error", "message": str(err)}

    ##################
    ##   Settings   ##
    ##################
    def get_setting(self, setting_id):
        logger.debug("API attempting to contact DB for get_setting...")
        try:
            self.cursor.execute("SELECT * FROM serversettings where id = %s", (setting_id,))
            result = self.cursor.fetchone()
            return {"status": "ok", "setting": result}
        except OperationalError as err:
            logger.error(f"Error fetching logging: {err}")
            return {"status": "error", "message": str(err)}

    def get_settings(self):
        logger.debug("API attempting to contact DB for get_setting...")
        try:
            self.cursor.execute("SELECT * FROM serversettings") # case sensitive
            result = self.cursor.fetchall()
            return {"status": "ok", "setting": result}
        except OperationalError as err:
            logger.error(f"Error fetching setting: {err}")
            return {"status": "error", "message": str(err)}


    def update_setting(self, setting_id, value):
        logger.debug(f"API attempting to contact DB for update_setting with setting ID:{setting_id} - Value:{value}")
        try:
            self.cursor.execute("UPDATE serversettings SET value = %s WHERE id = %s", (value, setting_id))
            return {"status": "ok", "message": "Setting updated successfully"}
        except OperationalError as err:
            logger.error(f"Error updating setting: {err}")
            return {"status": "error", "message": str(err)}

    def add_setting(self, name, value):
        logger.debug(f"API attempting to contact DB for add_setting with name:{name} - Value:{value}")
        try:
            self.cursor.execute("INSERT INTO serversettings (name, value) VALUES (%s, %s)", (name, value))
            return {"status": "ok", "message": "New setting added successfully"}
        except OperationalError as err:
            logger.error(f"Error adding new setting: {err}")
            return {"status": "error", "message": str(err)}

    def delete_setting(self, log_id):
        logger.debug(f"API attempting to contact DB for delete_setting with setting_ID:{log_id}")
        try:
            self.cursor.execute("DELETE FROM serversettings WHERE id = %s", (log_id,))
            return {"status": "ok", "message": f"Setting with ID {log_id} deleted successfully"}
        except OperationalError as err:
            logger.error(f"Error deleting setting: {err}")
            return {"status": "error", "message": str(err)}


    ##################
    ##   roles   ##
    ##################
    def get_role(self, role_id):
        logger.debug("API attempting to contact DB for get_role...")
        try:
            self.cursor.execute("SELECT * FROM roles where id = %s", (role_id,))
            result = self.cursor.fetchone()
            return {"status": "ok", "roles": result}
        except OperationalError as err:
            logger.error(f"Error fetching roles: {err}")
            return {"status": "error", "message": str(err)}

    def get_roles(self):
        logger.debug("API attempting to contact DB for get_roles...")
        try:
            self.cursor.execute("SELECT * FROM roles")
            result = self.cursor.fetchall()
            return {"status": "ok", "roles": result}
        except OperationalError as err:
            logger.error(f"Error fetching roles: {err}")
            return {"status": "error", "message": str(err)}

    def update_role(self, role_id, value):
        logger.debug(f"API attempting to contact DB for update_role with role ID:{role_id} - Value:{value}")
        try:
            self.cursor.execute("UPDATE roles SET value = %s WHERE id = %s", (value, role_id))
            return {"status": "ok", "message": "role updated successfully"}
        except OperationalError as err:
            logger.error(f"Error updating role: {err}")
            return {"status": "error", "message": str(err)}

    def add_role(self, name, value):
        logger.debug(f"API attempting to contact DB for add_role with name:{name} - Value:{value}")
        try:
            self.cursor.execute("INSERT INTO roles (name, value) VALUES (%s, %s)", (name, value))
            return {"status": "ok", "message": "New role added successfully"}
        except OperationalError as err:
            logger.error(f"Error adding new role: {err}")
            return {"status": "error", "message": str(err)}

    def delete_role(self, role_id):
        logger.debug(f"API attempting to contact DB for delete_role with role_ID:{role_id}")
        try:
            self.cursor.execute("DELETE FROM roles WHERE id = %s", (role_id,))
            return {"status": "ok", "message": f"role with ID {role_id} deleted successfully"}
        except OperationalError as err:
            logger.error(f"Error deleting role: {err}")
            return {"status": "error", "message": str(err)}

    ##################
    ##    Points    ##
    ##################
    def get_points_for_user(self, user_id):
        try:
            self.cursor.execute("SELECT points FROM users WHERE discord_id = %s", (user_id,))
            result = self.cursor.fetchone()
            if result is not None:
                return {"status": "ok", "points": result}
            else:
                return {"status": "error", "points": result}
        except OperationalError as err:
            logger.error(f"Error fetching points: {err}")
            return {"status": "error", "message": str(err)}

    def get_monthly_points_for_user(self, user_id):
        try:
            self.cursor.execute("SELECT montly_points FROM users WHERE discord_id = %s", (user_id))
            result = self.cursor.fetchone()
            if result is not None:
                return {"status": "ok", "monthly_points": result}
            else:
                return {"status": "error", "monthly_points": result}
        except OperationalError as err:
            logger.error(f"Error fetching monthly_points: {err}")
            return {"status": "error", "message": str(err)}

    def update_points(self, user_id, value):
        try:
            self.cursor.execute("UPDATE users SET points = points + %s WHERE discord_id = %s", (value, user_id))
            self.conn.commit()
            return {"status": "ok", "message": "points updated successfully"}
        except OperationalError as err:
            logger.error(f"Error updating points: {err}")
            self.conn.rollback()
            return {"status": "error", "message": str(err)}

    def add_user_to_points(self, user_id):
        try:
            self.cursor.execute(
                "INSERT INTO users (discord_id, points) VALUES (%s, 0) ON CONFLICT (discord_id) DO NOTHING;"
                , (user_id,)
            )
            # self.conn.commit()
            return {"status": "ok", "message": "New user added to 'points' successfully"}
        except OperationalError as err:
            logger.error(f"Error adding new user: {err}")
            # self.conn.rollback()
            return {"status": "error", "message": str(err)}

    def remove_user_from_points(self, user_id):
        try:
            self.cursor.execute("DELETE FROM users WHERE discord_id = %s", (user_id,))
            affected_rows = self.cursor.rowcount
            if affected_rows > 0:
                self.conn.commit()
                return {"status": "ok", "message": f"User with ID: {user_id} deleted successfully"}
            else:
                return {"status": "not_found", "message": f"No user found with ID: {user_id}"}
        except OperationalError as err:
            logger.error(f"Error deleting user: {err}")
            self.conn.rollback()
            return {"status": "error", "message": str(err)}

    def get_top_10(self):
        try:
            self.cursor.execute("SELECT discord_id, points FROM users ORDER BY points DESC LIMIT 10")
            result = self.cursor.fetchall()
            return {"status": "ok", "message": result}
        except OperationalError as err:
            logger.error(f"Error deleting user: {err}")
            self.conn.rollback()
            return {"status": "error", "message": str(err)}
