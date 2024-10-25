import os
import logging

def setup_logging():
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logs/"))       
    os.makedirs(log_dir, exist_ok=True)

    # Create a logger with propagation enabled
    logger = logging.getLogger("InpaintLogging")  
    logger.setLevel(logging.DEBUG)  

    # Handlers for different log levels
    info_handler = logging.FileHandler(os.path.join(log_dir, "info.log"))
    info_handler.setLevel(logging.INFO)

    warning_handler = logging.FileHandler(os.path.join(log_dir, "warning.log"))
    warning_handler.setLevel(logging.WARNING)

    error_handler = logging.FileHandler(os.path.join(log_dir, "error.log"))
    error_handler.setLevel(logging.ERROR)

    # Formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]")

    # Attach formatter to handlers
    info_handler.setFormatter(formatter)
    warning_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)

    # Attach handlers to the logger
    logger.addHandler(info_handler)
    logger.addHandler(warning_handler)
    logger.addHandler(error_handler)

    # Console logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Ensure that logs are propagated to the root logger
    logger.propagate = True

    return logger
