import logging
import os

# app.log will live in Part2_SystemsProduct, next to main.py
LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app.log")


def setup_logger():
    logger = logging.getLogger("currency_converter")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        # Already configured - don't add duplicate handlers
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger