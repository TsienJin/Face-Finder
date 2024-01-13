import os
import sqlite3


class DbDriver:

    connection:sqlite3.Connection

    def __init__(self):
        self.name="Driver"

    def connect(self):
        self.connection = sqlite3.connect(os.environ.get("DB_PATH"))

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
