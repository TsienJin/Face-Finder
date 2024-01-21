import os
import numpy as np
from typing import List
from deepface import DeepFace
from application.business_logic.biz_logic_parent import BizLogic
from application.database.faces_in_image_driver import FaceInImageDriver
from application.database.image_driver import ImageDriver
from application.models.faceInImage import FaceInImage
from application.models.image import Image
from PIL import Image as PillowImage, ImageOps as PillowImageOps


class BizScanForFaces(BizLogic):

    NAMED_BATCH_SIZE:int = 128  # number of file directories to keep in mem for each loop
    CACHE_DIR:str = f"{os.path.abspath('./application/cache/')}"
    THUMBNAIL_FACES_DIR:str = f"{os.path.abspath('./application/persist/thumbnails/faces')}"
    THUMBNAIL_IMAGES_DIR:str = f"{os.path.abspath('./application/persist/thumbnails/images')}"


    def __init__(self):
        super().__init__("Biz Scan For Faces")
        self.imageDriver = ImageDriver()

        if not os.path.exists(self.CACHE_DIR):
            os.mkdir(self.CACHE_DIR)

        if not os.path.exists(self.THUMBNAIL_FACES_DIR):
            os.mkdir(self.THUMBNAIL_FACES_DIR)

        if not os.path.exists(self.THUMBNAIL_IMAGES_DIR):
            os.mkdir(self.THUMBNAIL_IMAGES_DIR)

    def scan_indexed_files(self) -> None:
        self.logger.emit("Getting images")
        images = self.imageDriver.get_all_images()
        self.logger.emit("Fetched images from database")

        for image in images:
            try:

                facesInImageDriver = FaceInImageDriver()

                self.logger.emit(f"Processing image with ID: {image.id}")
                cached_image = self.__preprocess_create_jpg(image)
                faces = self.__scan_image(cached_image)
                faces = facesInImageDriver.write_faces_in_image_and_get_face_id(faces)

            except Exception as e:
                self.logger.emit(e.__str__())



    def __preprocess_create_jpg(self, image:Image) -> Image:
        assert image.id is not None, "Image id cannot be None, Image must be provided from DB!"

        newFilename = f"{image.id}.jpg"
        newFileDir = self.CACHE_DIR

        with PillowImage.open(f"{image.dir}{image.filename}") as img:
            img.save(fp=f"{self.CACHE_DIR}/{newFilename}", format="JPEG")

        return Image(id=image.id,filename=newFilename,dir=newFileDir)




    def __scan_image(self, image:Image) -> List[FaceInImage]:
        self.logger.emit(f"Scanning faces in image with ID: {image.id}")
        try:
            faces = DeepFace.represent(
                img_path=f"{image.dir}/{image.filename}",
                detector_backend='retinaface',
                enforce_detection=False
            )

            return [FaceInImage(
                encoding=np.array(face['embedding']),
                image_id=image.id,
                img_x_pos=face['facial_area']['x'],
                img_y_pos=face['facial_area']['y'],
                img_width=face['facial_area']['w'],
                img_height=face['facial_area']['h'],
            ) for face in faces]


        except Exception as e:
            self.logger.emit(e.__str__())
            return []


    def __create_thumbnail(self, image:Image) -> None:
        raise NotImplementedError

    def __create_face_thumbnail(self):
        raise NotImplementedError


