# logging_config.py

import os
import logging

def setup_logging():
    # Create a directory for logs if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    # Create a logger with propagation enabled
    logger = logging.getLogger("InpaintLoging")  # Use a specific name for your app
    logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG

    # Create handlers for different log levels
    info_handler = logging.FileHandler("logs/info.log")
    info_handler.setLevel(logging.INFO)

    warning_handler = logging.FileHandler("logs/warning.log")
    warning_handler.setLevel(logging.WARNING)

    error_handler = logging.FileHandler("logs/error.log")
    error_handler.setLevel(logging.ERROR)

    # Create a formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]")

    # Add formatter to handlers
    info_handler.setFormatter(formatter)
    warning_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(info_handler)
    logger.addHandler(warning_handler)
    logger.addHandler(error_handler)

    # Ensure that logs are propagated to the root logger
    logger.propagate = True

    return logger
