# from application.gui.controller import GuiController
from application.util.logger import LogSubscriber, Logger, LogEmitter


class BizLogic:

    logger:LogEmitter
    # guiController:GuiController

    def __init__(self, logger_source_name:str):
        self.logger = LogEmitter(logger_source_name)
        # self.guiController = GuiController()
