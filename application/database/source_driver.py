from typing import List

from application.database.db_driver import DbDriver
from application.util.logger import LogEmitter


class SourceDriver(DbDriver):

    def __init__(self):
        super().__init__()
        self.__init_table()

        self.logger = LogEmitter("Source Driver")

    def __init_table(self):
        self.connect()
        cursor = self.connection.cursor()

        cursor.execute("""
            create table if not exists sources (
                id integer primary key autoincrement,
                dir text unique not null 
            )
        """)

        self.connection.commit()
        self.close()


    def insert(self, source:str):
        self.connect()
        cursor = self.connection.cursor()

        cursor.execute("""
            insert or ignore into sources (dir) values (?)
        """, (source,))

        self.connection.commit()
        self.close()

    def get_all_sources(self) -> List[str]:
        self.connect()
        cursor = self.connection.cursor()

        res = cursor.execute("""
            select dir from sources
        """)

        all_sources = [src[0] for src in res.fetchall()]

        self.close()

        return all_sources

    def delete_sources(self, sources:List[str]):
        self.connect()
        cursor = self.connection.cursor()

        for source in sources:
            cursor.execute("""
                delete from sources where dir = (?)
            """, (source,))
            self.logger.emit(f"Deleted source {sources}")

        self.connection.commit()
        self.close()
        self.logger.emit(f"Deleted {len(sources)} source(s)")


