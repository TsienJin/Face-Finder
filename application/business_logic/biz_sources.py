from typing import Dict, List

from PyQt6.QtWidgets import QFileDialog

from application.business_logic.biz_logic_parent import BizLogic
from application.database.image_driver import ImageDriver
from application.database.source_driver import SourceDriver


class BizSources(BizLogic):

    def __init__(self):
        super().__init__(self.__class__.__name__)


    def get_sources_summary(self) -> Dict[str, int]:
        self.logger.emit("Fetching Sources Summary")
        sourceDriver = SourceDriver()
        sources:List[str] = sourceDriver.get_all_sources()

        res = {}

        for source in sources:
            res[source] = self.get_indexed_count_from_source(source)

        return res

    def get_indexed_count_from_source(self, source: str) -> int:
        self.logger.emit(f"Fetching image count for {source}")
        imageDriver = ImageDriver()
        return imageDriver.count_from_master_path(source)

    def add_source(self, source:str):
        self.logger.emit(f"Attempting to add source: {source}")
        sourceDriver = SourceDriver()
        sourceDriver.insert(source)
        self.logger.emit(f"Source added: {source}")

    def remove_sources(self, sources:List[str]):
        self.logger.emit(f"Attempting to remove {len(sources)} sources")
        sourceDriver = SourceDriver()
        sourceDriver.delete_sources(sources=sources)


