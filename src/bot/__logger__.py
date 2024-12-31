from __future__ import annotations
import os
import logging


def setup_logger(level, stream_logs) -> None:
    """
    Configures the logging system for the application.

    This function sets up the logging configuration for the application,
    allowing logs to be written to the console based on the specified
    logging level and whether streaming to the console is enabled.

    Parameters
    ----------
    level : int
        The logging level to be used for the main logs. This determines
        the severity of messages that will be logged.
    stream_logs : bool
        A flag indicating whether logs should be streamed to the console.
        If True, logs will be output to the console; otherwise, they will
        not be streamed.

    Returns
    -------
    None
        This function does not return any value.
    """
    log_formatter = logging.Formatter(
        ":: %(asctime)s :: %(levelname)s :: %(filename)s line %(lineno)s --- %(message)s"
        , "%m-%d %H:%M.%S")

    handlers: list[logging.Handler] = []
    if stream_logs:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        stream_handler.setLevel(level)
        handlers.append(stream_handler)

    logging.basicConfig(level=level, handlers=handlers)
