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
