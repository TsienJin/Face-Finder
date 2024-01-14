from typing import List


class Logger:

    subscribers: List['LogSubscriber'] = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Logger, cls).__new__(cls)
        return cls.instance

    def __init__(self, initial_subscribers:List['LogSubscriber']=[]):
        self.subscribers = initial_subscribers

    def subscribe(self, subscriber:'LogSubscriber'):
        self.subscribers.append(subscriber)

    def emit(self, message:str="", fallback_source:str=""):
        print(f"[LOGGER{f': {fallback_source}' if fallback_source else ''}] {message}")
        for subscriber in self.subscribers:
            subscriber.log_callback(f"[{fallback_source}] {message}")


class LogEmitter:

    def __init__(self, source:str):
        self.source = source
        self.logger = Logger()

    def emit(self, message:str):
        self.logger.emit(message, self.source)


class LogSubscriber:

    def log_callback(self, message):
        raise NotImplementedError
