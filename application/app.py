import os
import re

from dotenv import load_dotenv

from application.database.db_driver import DbDriver
from application.database.image_driver import ImageDriver
from application.objects.image import Image
from application.scan.probe import Probe, ProbeArgs
from application.util.image_dumper import ImageDumper



load_dotenv(".env")


def main():

    imageDriver = ImageDriver()

    probeArgs = ProbeArgs(
        path=os.environ.get("IMG_PARENT_FOLDER"),
        regex_filter=re.compile(r'.*.(jpg|jpeg|png|cr2)', re.IGNORECASE)
    )
    probe = Probe(probeArgs)
    image_tree = probe.get_all_dir()

    ImageDumper.dump_from_scantree(image_tree, imageDriver)


