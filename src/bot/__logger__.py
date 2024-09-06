from __future__ import annotations
import os
import logging


def setup_logger(level: int = int(os.getenv("LOG_LEVEL")), stream_logs: bool = False) -> None:
    """
    Sets up the service logs
    Parameters
    ----------
    level : int
        Level to log in the main logs
    stream_logs : bool
        Flag to stream the logs to the console
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
