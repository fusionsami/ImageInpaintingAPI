# logging_config.py

import os
import logging

def setup_logging():
    # directory for logs if it doesn't exist
    os.makedirs("../logs", exist_ok=True)

    # a logger with propagation enabled
    logger = logging.getLogger("InpaintLoging")  # Use a specific name for your app
    logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG

    # handlers for different log levels
    info_handler = logging.FileHandler("../logs/info.log")
    info_handler.setLevel(logging.INFO)

    warning_handler = logging.FileHandler("../logs/warning.log")
    warning_handler.setLevel(logging.WARNING)

    error_handler = logging.FileHandler("../logs/error.log")
    error_handler.setLevel(logging.ERROR)

    # formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]")

    # formatter to handlers
    info_handler.setFormatter(formatter)
    warning_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)

    # handlers to the logger
    logger.addHandler(info_handler)
    logger.addHandler(warning_handler)
    logger.addHandler(error_handler)

    # console logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Ensure that logs are propagated to the root logger
    logger.propagate = True

    return logger
