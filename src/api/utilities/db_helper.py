import os
import psycopg
from psycopg import OperationalError


class DB:
    def __init__(self):
        self.conn = psycopg.connect(
                dbname=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                host=os.getenv('POSTGRES_HOST')
            )
        self.cursor = self.conn.cursor()

    def db_health_check(self):
        try:
            self.conn.close()
            return True
        except OperationalError as err:
            return {"error": {err}, "status": False}

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error executing query: {e}")
            self.conn.rollback()
            return False

    def fetch_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def create(self, table, data):
        columns = ', '.join(data.keys())
        values = ', '.join('%s' for _ in data.values())
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        return self.execute_query(query, tuple(data.values()))

    def read(self, table, condition=None, params=None):
        condition = f"WHERE {condition}" if condition else ""
        query = f"SELECT * FROM {table} {condition}"
        return self.fetch_query(query, params)

    def update(self, table, data, condition, params=None):
        set_clause = ', '.join([f"{column} = %s" for column in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        return self.execute_query(query, tuple(data.values()) + params)

    def delete(self, table, condition, params=None):
        query = f"DELETE FROM {table} WHERE {condition}"
        return self.execute_query(query, params)


# # Example Usage:
# # Replace 'your_connection_string' with the actual PostgreSQL connection string
# connection_string = "your_connection_string"
# db_wrapper = SimpleDatabaseWrapper(connection_string)
#
# # Create
# user_data = {"name": "John Doe", "email": "john@example.com"}
# db_wrapper.create("users", user_data)
#
# # Read
# all_users = db_wrapper.read("users")
# print("All Users:", all_users)
#
# # Update
# update_data = {"name": "Updated John", "email": "updated_john@example.com"}
# db_wrapper.update("users", update_data, "name = %s", ("John Doe",))
#
# # Read after update
# updated_users = db_wrapper.read("users", "name = %s", ("Updated John",))
# print("Updated Users:", updated_users)
#
# # Delete
# db_wrapper.delete("users", "name = %s", ("Updated John",))
#
# # Read after delete
# remaining_users = db_wrapper.read("users")
# print("Remaining Users:", remaining_users)
#
# # Close the connection
# db_wrapper.conn.close()
