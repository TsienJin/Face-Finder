import sys
import os
import re
import glob
from concurrent.futures import ThreadPoolExecutor, as_completed

from typing import Pattern, Dict

from application.objects.image import Image
from application.scan.scan_tree import ScanTree
from application.util.logger import LogEmitter
from application.util.verify_files_at_each_level_callback import VerifyFilesAtEachLevelCallback


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
    logger: LogEmitter

    def __init__(self, probeArgs: ProbeArgs):
        self.probeArgs = probeArgs
        self.pattern = re.compile(probeArgs.regex_filter)
        self.logger = LogEmitter("Probe")


    def __get_all_dir_parallel(self, parent: ScanTree, verify_files_at_each_level:VerifyFilesAtEachLevelCallback) -> ScanTree:
        self.logger.emit(f"Scanning {parent.full_path}")

        # Create thread pool
        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = []

            # Iterate over items in path
            for item in os.listdir(parent.full_path):

                # Get absolute path
                item_path = os.path.join(parent.full_path, item)

                # If item is not a directory
                if not os.path.isdir(item_path):
                    # and matches regex
                    if self.pattern.match(item):
                        # Add file to ScanTree.files
                        parent.files.append(Image(id=None, dir=parent.full_path + '/', filename=item))
                else:
                    # Submit directory scanning tasks to the thread pool
                    future = executor.submit(self.__get_all_dir_parallel, ScanTree(full_path=item_path), verify_files_at_each_level)
                    futures.append(future)

            if len(parent.files) > 0:
                verify_files_at_each_level(dir=parent.full_path + '/', images=parent.files)



            # Wait for all submitted tasks to complete
            for future in as_completed(futures):
                child_tree = future.result()
                parent.child_trees.append(child_tree)

        return parent


    def create_scan_tree(self, verify_files_at_each_level:VerifyFilesAtEachLevelCallback) -> ScanTree:
        self.logger.emit(f"Creating scan tree for {os.path.abspath(self.probeArgs.path)}")
        return self.__get_all_dir_parallel(parent=ScanTree(full_path=os.path.abspath(self.probeArgs.path)), verify_files_at_each_level=verify_files_at_each_level)
