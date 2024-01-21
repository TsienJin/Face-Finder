from typing import List

from application.models.image import Image


class ScanTree:
    full_path: str = ""
    files: List[Image] = []
    child_trees: List['ScanTree'] = []

    def __init__(self, full_path: str = "", files:List[str]=None, child_trees:List['ScanTree']=None):

        if child_trees is None:
            child_trees = []
        if files is None:
            files = []

        self.full_path = full_path
        self.files = files
        self.child_trees = child_trees

    def __str__(self):
        return f"""[{self.full_path}]\tFiles: {len(self.files)}\tChild_Dir: {len(self.child_trees)}"""




