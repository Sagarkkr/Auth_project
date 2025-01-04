import logging
from logging import config, getLogger
from typing import Any

from src.core.config import settings


class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[94m",  # Blue
        logging.INFO: "\033[92m",  # Green
        logging.WARNING: "\033[93m",  # Yellow
        logging.ERROR: "\033[91m",  # Red
        logging.CRITICAL: "\033[95m",  # Magenta
    }
    RESET_COLOR = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelno, self.RESET_COLOR)
        record.colorized_msg = color + super().format(record) + self.RESET_COLOR
        return record.colorized_msg


def setup_logger() -> Any:
    config.fileConfig(settings.DEFAULT_LOGGER_CONFIG_PATH)

    for handler in logging.getLogger().handlers:
        formatter = ColoredFormatter(fmt=handler.formatter._fmt)
        handler.setFormatter(formatter)


_LOG_LEVEL = settings.LOG_LEVEL

logger = getLogger("root")
apilogger = getLogger("api")
dblogger = getLogger("database")
httplogger = getLogger("http")

logger.setLevel(_LOG_LEVEL)
apilogger.setLevel(_LOG_LEVEL)
dblogger.setLevel(_LOG_LEVEL)
httplogger.setLevel(_LOG_LEVEL)
