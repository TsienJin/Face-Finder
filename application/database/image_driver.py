from typing import List

from application.database.db_driver import DbDriver
from application.objects.image import Image



class ImageDriver(DbDriver):

    def __init__(self):
        super().__init__()
        self.__init_table()

    def __init_table(self):
        self.connect()
        cursor = self.connection.cursor()

        cursor.execute("""
            create table if not exists images (
                id integer primary key autoincrement,
                dir text not null,
                filename text not null
            );
        """)

        cursor.execute("""
            create index if not exists image_path_index on images(dir);
        """)

        cursor.execute("""
            create unique index if not exists image_filename_index on images(dir, filename);
        """)

        self.connection.commit()
        self.close()

    def insert_image(self, img:Image):
        self.connect()
        cursor = self.connection.cursor()

        cursor.execute("""
            insert or ignore into images(dir, filename) values(?, ?)
        """, (img.dir, img.filename))

        self.connection.commit()
        self.close()

    def insert_image_list(self, img_list:List[Image]):
        self.connect()
        cursor = self.connection.cursor()

        for img in img_list:
            cursor.execute("""
                insert or ignore into images(dir, filename) values(?, ?)
            """, (img.dir, img.filename))

        self.connection.commit()
        self.close()

    def delete_image_list(self, img_list:List[Image]):
        self.connect()
        cursor = self.connection.cursor()

        for img in img_list:
            cursor.execute("""
                delete from images where dir = (?) and filename = (?)
            """, (img.dir, img.filename,))

        self.connection.commit()
        self.close()

    def delete_image_from_master_path(self, master_path:str) -> None:
        self.connect()
        cursor = self.connection.cursor()

        cursor.execute("""
            delete from images where dir like (?)
        """, (f"{master_path}%",))

        self.connection.commit()
        self.close()

    def count_from_master_path(self, master_path:str) -> int:
        self.connect()
        cursor = self.connection.cursor()

        res = cursor.execute("""
            select count(*) from images where dir like (?)
        """, (f"{master_path}%",))

        count = res.fetchone()[0]

        self.close()

        return count

    def get_image_names_in_path(self, path:str) -> List[str]:
        self.connect()
        cursor = self.connection.cursor()
        res = cursor.execute("""
            select filename from images where dir = (?)
        """, (path,))

        filenames = [file[0] for file in res.fetchall()]
        self.close()
        return filenames

