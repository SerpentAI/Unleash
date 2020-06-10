import logging
import rich.logging


logging.basicConfig(
    format="%(message)s", datefmt="[Unleash]", handlers=[rich.logging.RichHandler()]
)


class Logger:
    def __init__(self, level="INFO"):
        if level not in self.levels:
            level = "INFO"

        self.logger = logging.getLogger("unleash")
        self.logger.setLevel(level)

    @property
    def levels(self):
        return "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"

    def set_level(self, level="INFO"):
        if level not in self.levels:
            return False

        self.logger.setLevel(level)

        return True

    def critical(self, message):
        self.logger.critical(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)


# TODO: Consider logger level from config file or CLI args
logger = Logger(level="DEBUG")
