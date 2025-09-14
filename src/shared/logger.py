import logging
import os
from datetime import datetime
from typing import Optional


class Logger:
    _instance: Optional["Logger"] = None
    _logger: Optional[logging.Logger] = None

    def __new__(cls) -> "Logger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._logger is None:
            self._setup_logger()

    def _setup_logger(self):
        self._logger = logging.getLogger("biblioteca_liskov")
        self._logger.setLevel(logging.INFO)

        if not os.path.exists("logs"):
            os.makedirs("logs")

        log_filename = f"logs/biblioteca_{datetime.now().strftime('%Y%m%d')}.log"

        file_handler = logging.FileHandler(log_filename, encoding="utf-8")
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)

    def info(self, message: str):
        if self._logger:
            self._logger.info(message)

    def warning(self, message: str):
        if self._logger:
            self._logger.warning(message)

    def error(self, message: str):
        if self._logger:
            self._logger.error(message)

    def debug(self, message: str):
        if self._logger:
            self._logger.debug(message)


def get_logger() -> Logger:
    return Logger()
