from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QHBoxLayout, QMenuBar

from application.gui.views.view_main.widgets.right_panel import RightPanel


class ViewMain(QMainWindow):
    widget: QWidget
    config_tab: RightPanel
    menubar: QMenuBar


    def __init__(self):
        super().__init__()

        self.setWindowTitle("Face Finder")
        self.set_contents()

    def set_contents(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.config_tab = RightPanel()
        layout.addWidget(self.config_tab)

        self.widget = QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)
