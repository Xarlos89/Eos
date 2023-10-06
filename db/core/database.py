import psycopg2
from syncronize_db import sync

class DB:
    def __init__(self, db_string):
        self.conn = psycopg2.connect(db_string)
        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()

    def synchronise(self, discord_client):
        sync(discord_client)

    def select_one(self, query, *data):
        if data:
            self.cur.execute(query, data)
        else:
            self.cur.execute(query)
        data = self.cur.fetchone()
        self.conn.commit()
        self.conn.close()
        return data

    def select_all(self, query, *data):
        if data:
            self.cur.execute(query, data)
        else:
            self.cur.execute(query)
        data = self.cur.fetchall()
        self.conn.commit()
        self.conn.close()
        return data

    def update(self, query, data):
        self.cur.execute(query, (data,))
        self.conn.commit()
        self.conn.close()

    def insert(self, query, data):
        self.cur.execute(query, (data,))
        self.conn.commit()
        self.conn.close()







