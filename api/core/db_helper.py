import os
import logging
import psycopg
from psycopg import OperationalError

log = logging.getLogger(__name__)

class DB:
    def __init__(self):
        self.conn = psycopg.connect(
                dbname=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                host=os.getenv('POSTGRES_HOST')
            )
        self.cursor = self.conn.cursor()


    ##################
    ## Healthchecks ##
    ##################
    def database_health_check(self):
        try:
            self.cursor.execute("SELECT 1")
            result = self.cursor.fetchone()
            if result:
                return {"status": "ok"}

        except OperationalError as err:
            log.info(f"DB Healthcheck - 500 - {err}")
            self.conn.close()
            return {"status": "unhealthy", "error": {err}}

    ##################
    ##   Settings   ##
    ##################
    def get_settings(self):
        try:
            self.cursor.execute("SELECT * FROM settings")
            result = self.cursor.fetchall()
            return {"status": "ok", "settings": result}
        except OperationalError as err:
            log.error(f"Error fetching settings: {err}")
            return {"status": "error", "message": str(err)}

    def update_setting(self, setting_id, value):
        try:
            self.cursor.execute("UPDATE settings SET value = %s WHERE id = %s", (value, setting_id))
            self.conn.commit()
            return {"status": "ok", "message": "Setting updated successfully"}
        except OperationalError as err:
            log.error(f"Error updating setting: {err}")
            self.conn.rollback()
            return {"status": "error", "message": str(err)}

    def add_setting(self, name, value):
        try:
            self.cursor.execute("INSERT INTO settings (name, value) VALUES (%s, %s)", (name, value))
            self.conn.commit()
            return {"status": "ok", "message": "New setting added successfully"}
        except OperationalError as err:
            log.error(f"Error adding new setting: {err}")
            self.conn.rollback()
            return {"status": "error", "message": str(err)}

    def delete_setting(self, setting_id):
        try:
            self.cursor.execute("DELETE FROM settings WHERE id = %s", (setting_id,))
            affected_rows = self.cursor.rowcount
            if affected_rows > 0:
                self.conn.commit()
                return {"status": "ok", "message": f"Setting with ID {setting_id} deleted successfully"}
            else:
                return {"status": "not_found", "message": f"No setting found with ID {setting_id}"}
        except OperationalError as err:
            log.error(f"Error deleting setting: {err}")
            self.conn.rollback()
            return {"status": "error", "message": str(err)}
