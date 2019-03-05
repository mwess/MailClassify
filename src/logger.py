import os

class CustomLogger():

    default_logger_file = 'data/logging.txt'

    def __init__(self, log_file):
        self._log_file = log_file

    @classmethod
    def from_default_file(cls):
        return cls(CustomLogger.default_logger_file)

    @staticmethod
    def log_result(result: str):
        logger = CustomLogger.from_default_file()
        logger.add_entry(result)

    def add_entry(self, entry: str, with_newline=True):
        with open(self._log_file, 'a+') as f:
            f.write(entry)
            if with_newline:
                f.write('\n')

