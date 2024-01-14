from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QHBoxLayout, QMenuBar

from application.gui.views.view_main.widgets.config_tab import ConfigTab


class ViewMain(QMainWindow):
    widget: QWidget
    config_tab: ConfigTab
    menubar: QMenuBar


    def __init__(self):
        super().__init__()

        self.setWindowTitle("Face Finder")
        self.set_contents()

    def set_contents(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("Label"))

        self.config_tab = ConfigTab()
        layout.addWidget(self.config_tab)

        self.widget = QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)
