import os
import re

import numpy as np
from dotenv import load_dotenv

from application.business_logic.biz_scan_for_faces import BizScanForFaces
from application.database.db_driver import DbDriver
from application.database.image_driver import ImageDriver
from application.database.source_driver import SourceDriver
from application.models.faceInImage import FaceInImage
from application.models.image import Image
from application.scan.probe import Probe, ProbeArgs
from application.util.image_dumper import ImageDumper
from application.gui.controller import GuiController
from application.util.logger import Logger, LogEmitter

load_dotenv(".env")


def main():
    # logger = LogEmitter("APP.PY")
    # logger.emit("Starting application")
    # gui = GuiController()
    # logger.emit("Quiting application")

    # Initialise tables
    # sourceDriver = SourceDriver()
    imageDriver = ImageDriver()
    # print(imageDriver.get_all_images())
    bizScanFace = BizScanForFaces()
    bizScanFace.scan_indexed_files()
    #


    # fim = FaceInImage(encoding=np.array([1,2,3,]))


if __name__ == "__main__":
    main()
