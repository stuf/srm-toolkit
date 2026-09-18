import getpass
import logging
from tempfile import gettempdir
from pathlib import Path

from .generic import get_name


def setup_logger(logger: logging.Logger):
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(fmt='{levelname:>8} {name:>20} | {message}',
                                  style='{')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)


def update_logger(logger: logging.Logger):
    pass
