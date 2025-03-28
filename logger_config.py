"""
Logging module for unified logging configuration.

This module sets up a unified logging configuration that can be used across
different parts of a project. It defines a logger that logs messages both to
the console and to a file. The file name and log level can be customized.

Functions:
    get_logger: Sets up and returns a logger instance.

Example usage:
    logger = get_logger("my_logger")
    logger.info("This is an info message.")
"""

import logging
import sys


def get_logger(logger_name: str, log_file: str = 'app.log',
               log_level_console: int = logging.WARNING,
               log_level_file: int = logging.INFO,
               file_write: bool = True) -> logging.Logger:
    """
    Sets up and returns a logger instance.

    This function creates a logger that outputs log messages to both the
    console and a log file. It can be configured with a custom file name
    and log level.

    Parameters:
        logger_name (str): The name of the logger.
        log_file (str): The file where log messages will be written. Default is 'app.log'.
        log_level (int): The logging level. Default is logging.INFO.

    Returns:
        logging.Logger: A configured logger instance.

    Example:
        logger = get_logger("my_logger")
        logger.debug("This is a debug message.")
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(min(log_level_console, log_level_file))

    formatter = logging.Formatter('%(asctime)s - %(module)s (%(name)s) - '
                                  '%(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')

    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(log_level_console)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if file_write:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(log_level_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
