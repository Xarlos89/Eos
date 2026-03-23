"""
A simple monthly Yapathon, gives the yapper role to the member with the most points every month.
"""

from apsheduler.schedulers.background import BackgroundScheduler

import logging

logger = logging.getLogger(__name__)


DATE = "1"
TIME_HOUR = "0"
TIME_MINUTE = "0"


async def make_a_new_yapper():
    pass

scheduler = BackgroundScheduler()
