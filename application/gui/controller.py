import sys
import webbrowser

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar

from application.gui.views.view_logging import ViewLogging
from application.gui.views.view_main.view_main import ViewMain


class GuiController:
    app: QApplication
    window: QMainWindow

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GuiController, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.logging_window = None
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Face Finder")
        self.__set_window(ViewMain())
        self.start()


    def __set_window(self, window:QMainWindow):
        self.window = window
        self.__config_menu_bar(self.window.menuBar())
        self.window.show()

    def __config_menu_bar(self, menuBar: QMenuBar):

        # Window menu actions
        window_menu = menuBar.addMenu("&Windows")
        action_open_logging = QAction("Logs", self.window)
        action_open_logging.triggered.connect(self.open_window_logging)
        action_open_logging.setShortcut("Ctrl+l")
        window_menu.addAction(action_open_logging)


        # GitHub menu actions
        github_menu = menuBar.addMenu("&GitHub")

        action_open_repo = QAction("&View Repository", self.window)
        action_open_repo.triggered.connect(lambda: webbrowser.open("https://github.com/TsienJin/Face-Finder?tab=readme-ov-file"))
        github_menu.addAction(action_open_repo)

        github_menu.addSeparator()

        action_report_bug = QAction("&Report Issue", self.window)
        action_report_bug.triggered.connect(lambda: webbrowser.open("https://github.com/TsienJin/Face-Finder/issues"))
        github_menu.addAction(action_report_bug)

    def open_window_logging(self):
        self.logging_window = ViewLogging()
        self.logging_window.show()



    def start(self):
        self.app.exec()

    def quit(self):
        self.app.quit()
