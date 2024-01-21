import os
import sqlite3
import numpy as np
import io


class DbDriver:

    connection:sqlite3.Connection

    def __init__(self):
        self.name="Driver"

        """
        https://stackoverflow.com/questions/18621513/python-insert-numpy-array-into-sqlite3-database
        """
        sqlite3.register_adapter(np.ndarray, DbDriver.__np_arr_to_text)
        sqlite3.register_converter("array", DbDriver.__text_to_np_arr)

    def __init_table(self):
        raise NotImplementedError

    @staticmethod
    def __np_arr_to_text(arr):
        out = io.BytesIO()
        np.save(out, arr)
        out.seek(0)
        return sqlite3.Binary(out.read())

    @staticmethod
    def __text_to_np_arr(text):
        out = io.BytesIO(text)
        out.seek(0)
        return np.load(out)

    def connect(self):
        self.connection = sqlite3.connect(os.environ.get("DB_PATH"))

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
