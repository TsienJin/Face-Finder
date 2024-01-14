import os
import re

from dotenv import load_dotenv

from application.database.db_driver import DbDriver
from application.database.image_driver import ImageDriver
from application.database.source_driver import SourceDriver
from application.objects.image import Image
from application.scan.probe import Probe, ProbeArgs
from application.util.image_dumper import ImageDumper
from application.gui.controller import GuiController
from application.util.logger import Logger, LogEmitter

load_dotenv(".env")


def main():

    # Initialise tables
    sourceDriver = SourceDriver()
    imageDriver = ImageDriver()

    logger = LogEmitter("APP.PY")
    logger.emit("Starting application")
    gui = GuiController()
    logger.emit("Quiting application")


if __name__ == "__main__":
    main()
