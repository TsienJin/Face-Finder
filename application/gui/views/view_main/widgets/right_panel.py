import os
import re

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel, QListWidget, QHBoxLayout, QPushButton, \
    QPlainTextEdit, QTreeWidget, QFileDialog, QTreeWidgetItem

from application.business_logic.biz_images import BizImages
from application.business_logic.biz_sources import BizSources
from application.database.image_driver import ImageDriver
from application.scan.probe import ProbeArgs, Probe
from application.util.image_dumper import ImageDumper
from application.util.logger import LogSubscriber, Logger


class ConfigPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.paths = Config_Paths()
        layout.addWidget(self.paths)

        self.setLayout(layout)


class Config_Paths(QGroupBox):

    def __init__(self):
        super().__init__("Paths")

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

