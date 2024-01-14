import os
import re

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel, QListWidget, QHBoxLayout, QPushButton, \
    QPlainTextEdit, QTreeWidget, QFileDialog, QTreeWidgetItem

from application.business_logic.biz_images import BizImages
from application.business_logic.biz_sources import BizSources
from application.database.image_driver import ImageDriver
from application.scan.probe import ProbeArgs, Probe
from application.util.image_dumper import ImageDumper
from application.util.logger import LogSubscriber, Logger, LogEmitter


class RightPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.paths = Source_Path_Group()
        self.ai_control = Face_Ai_Control_Group()
        self.filter = Filter_Face_Group()
        layout.addWidget(self.paths)
        layout.addWidget(self.ai_control)
        layout.addWidget(self.filter)

        self.setLayout(layout)


class Source_Path_Group(QGroupBox):

    def __init__(self):
        super().__init__("Paths")
        self.logger = LogEmitter("Source Path Group")

        layout = QVBoxLayout()

        self.treeWidget = QTreeWidget()
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setHeaderLabels(['Indexed Images', 'Path'])
        self.treeWidget.resizeColumnToContents(0)

        layout.addWidget(self.treeWidget)

        self.scan_source_button = QPushButton("Scan and Index Directories")
        self.add_source_button = QPushButton("Add Source Directory")
        self.remove_source_button = QPushButton("Remove Selected Directory")
        layout.addWidget(self.scan_source_button)
        layout.addWidget(self.add_source_button)
        layout.addWidget(self.remove_source_button)

        self.setLayout(layout)

        self.__configure_bindings()
        self.update_list()

    def __configure_bindings(self):
        self.scan_source_button.clicked.connect(self.scanSourceCallback)
        self.add_source_button.clicked.connect(self.addSourceCallback)
        self.remove_source_button.clicked.connect(self.removeSourceCallback)

    def update_list(self):
        bizSources = BizSources()
        summary = bizSources.get_sources_summary()
        self.logger.emit("Updating source list")
        self.treeWidget.clear()

        for source, count in summary.items():
            entry = QTreeWidgetItem(self.treeWidget)
            entry.setText(0, source)
            entry.setText(1, f"{count}")


    def scanSourceCallback(self):
        bizSources = BizSources()
        bizImages = BizImages()
        imageDriver = ImageDriver()
        summary = bizSources.get_sources_summary()

        for source, _ in summary.items():
            self.logger.emit(f"Initializing scan on {source}")
            probeArgs = ProbeArgs(
                path=source,
                regex_filter=re.compile(r'.*.(jpg|jpeg|png|cr2|tif|dng)', re.IGNORECASE)
            )

            probe = Probe(probeArgs)
            probe.create_scan_tree(bizImages.verifyFilesAtEachLevelCallback)

        self.update_list()

    def addSourceCallback(self):
        source_dir = QFileDialog.getExistingDirectory(self, "Select Directory")
        if source_dir:
            bizSources = BizSources()
            bizSources.add_source(source_dir+'/')
            self.update_list()

    def removeSourceCallback(self):
        bizSources = BizSources()
        bizImages = BizImages()

        selected_items = self.treeWidget.selectedItems()
        paths_to_remove = [path.text(0) for path in selected_items]

        bizSources.remove_sources(paths_to_remove)
        bizImages.remove_images_from_master_paths(paths_to_remove)
        self.update_list()


class Face_Ai_Control_Group(QGroupBox):
    def __init__(self):
        super().__init__("AI Control")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("AI Control"))
        self.setLayout(layout)


class Filter_Face_Group(QGroupBox):

    def __init__(self):
        super().__init__("Filter by Face")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Filter by faces"))
        self.setLayout(layout)



