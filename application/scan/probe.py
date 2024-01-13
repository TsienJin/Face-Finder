import sys
import os
import re
import glob

from typing import Pattern, Dict

from application.objects.image import Image
from application.scan.scan_tree import ScanTree


class ProbeArgs:
    path: str
    regex_filter: Pattern[str]

    def __init__(self, path:str, regex_filter:Pattern[str]):
        assert path[-1] == "/" or path[-1] == "//", "Path must terminate with `/` or `//` to be considered a directory!"

        self.path = path
        self.regex_filter = regex_filter


class Probe:
    path: str
    pattern:Pattern

    def __init__(self, probeArgs: ProbeArgs):
        self.probeArgs = probeArgs
        self.pattern = re.compile(probeArgs.regex_filter)

    def __get_all_dir(self, parent:ScanTree) -> ScanTree:

        # Iterates over all items in current directory
        for item in os.listdir(parent.full_path):

            # Checks if the item is a file and NOT a dir
            if not os.path.isdir(os.path.join(parent.full_path, item)):

                # Checks if the file matches the regex provided
                if self.pattern.match(item):
                    # append to parent node
                    parent.files.append(Image(id=None, dir=parent.full_path, filename=item))

            # When item is a directory
            else:
                # recursively call this method
                parent.child_trees.append(self.__get_all_dir(ScanTree(full_path=os.path.join(parent.full_path, item))))

        return parent


    def get_all_dir(self) -> ScanTree:
        return self.__get_all_dir(parent=ScanTree(full_path=os.path.abspath(self.probeArgs.path)))
