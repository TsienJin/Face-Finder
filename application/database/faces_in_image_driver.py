from typing import List

from application.database.db_driver import DbDriver
from application.models.faceInImage import FaceInImage


class FaceInImageDriver(DbDriver):
    # TODO implement with chromaDB instead

    def __init__(self):
        super().__init__()
        self.__init_table()

    def __init_table(self):
        self.connect()
        cursor = self.connection.cursor()

        cursor.execute("""
            create table if not exists faces_in_image (
                id integer primary key autoincrement,
                image_id integer not null references images(id),
                img_x_pos integer not null,
                img_y_pos integer not null,
                img_width integer not null,
                img_height integer not null,
                encoding array not null
            );
        """)

        cursor.execute("""
            create index if not exists image_id_index on faces_in_image(image_id);
        """)

        self.connection.commit()
        self.close()

    def write_faces_in_image_and_get_face_id(self, facesInImage:List[FaceInImage]) -> List[FaceInImage]:
        newArr:List[FaceInImage] = []

        self.connect()
        cursor = self.connection.cursor()

        for fii in facesInImage:
            print(fii)
            cursor.execute("""
                insert into faces_in_image (image_id, img_x_pos, img_y_pos, img_width, img_height, encoding) values (?,?,?,?,?,?)
                returning id;
            """, (fii.image_id, fii.img_x_pos, fii.img_y_pos, fii.img_width, fii.img_height, fii.encoding))
            fii.id = cursor.fetchone()[0]
            newArr.append(fii)

        self.commit()
        self.close()

        return newArr

    def get_all_faces_in_image(self) -> List[FaceInImage]:
        self.connect()
        cursor = self.connection.cursor()

        res = cursor.execute("""
            select * from faces_in_image;
        """)
        all_faces = res.fetchall()

        self.close()

        return [FaceInImage(
            id=fii[0],
            image_id=fii[1],
            img_x_pos=fii[2],
            img_y_pos=fii[3],
            img_width=fii[4],
            img_height=fii[5],
            encoding=fii[6]
        ) for fii in all_faces]
