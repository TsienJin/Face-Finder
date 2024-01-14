from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPlainTextEdit

from application.util.logger import LogSubscriber, Logger


class ViewLogging(QMainWindow, LogSubscriber):
    def __init__(self):
        super().__init__()

        self.logger = Logger()
        self.logger.subscribe(self)
        self.source = "LOGGING WINDOW"

        self.setWindowTitle("Logs")

        widget = QWidget()
        layout = QVBoxLayout()

        layout = QVBoxLayout()

        self.log_element = QPlainTextEdit()
        self.log_element.setReadOnly(True)

        layout.addWidget(self.log_element)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.logger.emit("Logging window initialized!")

    def log_callback(self, message):
        self.log_element.appendPlainText(message)
