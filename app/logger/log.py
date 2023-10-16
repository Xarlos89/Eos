"""
Controls the logger for the entire application.
Also, the logger level is controlled here
"""
import logging
import os
import pathlib
import json



log_file_path = pathlib.Path('app', 'logger', 'logs.txt')
logging.basicConfig(filename=log_file_path,
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M.%S',
                    filemode='w')

logger = logging.getLogger()
"""
10 = DEBUG
20 = INFO
30 = WARN
50 = CRITICAL
"""
logger.setLevel(int(os.getenv('LOG_LEVEL')))


def debug(thing: object):
    """ Logs at the debug level """
    logger.debug(thing)


def info(thing: object):
    """ Logs at the info level """
    print(thing)
    logger.info(thing)


def warn(thing: object):
    """ Logs at the warn level """
    print(thing)
    logger.warning(thing)


def critical(thing: object):
    """ Logs at the critical level """
    print(thing)
    logger.critical(thing)