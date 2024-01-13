
from application.scan.scan_tree import ScanTree
from application.database.image_driver import ImageDriver


class ImageDumper:
    """
    Class to dump images from various sources to ImageDriver
    """

    @staticmethod
    def dump_from_scantree(tree:ScanTree, driver:ImageDriver):
        for child_tree in tree.child_trees:
            ImageDumper.dump_from_scantree(child_tree, driver)

        driver.insert_image_list(tree.files)
