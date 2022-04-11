import logging


class Logger(logging.Logger):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.setLevel(logging.DEBUG)
        self.addHandler(Logger._create_handler())

    @staticmethod
    def _create_handler():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s:%(levelname)-7s: %(message)s')
        handler.setFormatter(formatter)
        return handler


logger = Logger(__package__)
