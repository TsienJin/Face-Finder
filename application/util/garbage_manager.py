from application.util.logger import LogEmitter


class GarbageManager:


    instance = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GarbageManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.logger = LogEmitter("Garbage Manager")

    def remove_file(self, file:str) -> None:
        raise NotImplementedError
