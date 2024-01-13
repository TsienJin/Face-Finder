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
