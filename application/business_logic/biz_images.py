from typing import List

from application.business_logic.biz_logic_parent import BizLogic
from application.database.image_driver import ImageDriver
from application.objects.image import Image
from application.util.logger import LogEmitter


class BizImages(BizLogic):

    imageDriver:ImageDriver

    def __init__(self):
        super().__init__("BizImages")
        self.imageDriver = ImageDriver()

    @staticmethod
    def verifyFilesAtEachLevelCallback(dir: str, images: List[Image]):
        """
        This method will delete the entries that are no longer in the scan tree,
        and add files that have appeared in the scan tree.
        :param images:
        :param dir:
        :return:
        """
        logger = LogEmitter("BizImages Callback")
        try:
            imageDriver = ImageDriver()
            current_image_names = imageDriver.get_image_names_in_path(dir)

            if len(current_image_names) > 0:
                # print(current_image_names)
                current_images = [Image(dir=dir, filename=name) for name in current_image_names]
                to_delete = [_to_delete for _to_delete in current_images if _to_delete not in images]
                to_insert = [_to_insert for _to_insert in images if _to_insert not in current_images]
                imageDriver.delete_image_list(to_delete)
                imageDriver.insert_image_list(to_insert)
            else:
                imageDriver.insert_image_list(images)
        except Exception as e:
            logger.emit(e.__str__())


    def remove_images_from_master_paths(self, master_paths:List[str]):
        for path in master_paths:
            self.imageDriver.delete_image_from_master_path(path)

