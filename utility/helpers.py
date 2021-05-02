from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler
from pytz import timezone
import logging


def log(level: int, log_file: str):
    logger = logging.getLogger('Bot Log')
    logger.setLevel(level)
    handler = RotatingFileHandler(f'../{log_file}', maxBytes = 500000, backupCount = 5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

# measures the amount of idle time between now and then (the given timestamp, which should be user's last message or
# last active in voice comms.


def check_idle_time(ts: datetime):
    central_tz = timezone('US/Central')
    current_time = datetime.now(central_tz)
    difference = current_time - ts
    duration_in_seconds = difference.total_seconds()
    days = timedelta(seconds = duration_in_seconds).days
    remaining_seconds = timedelta(seconds = duration_in_seconds).seconds
    hours = remaining_seconds // 3600
    minutes = (remaining_seconds // 60) % 60

    return { 'days': days, 'hours': hours, 'minutes': minutes }
