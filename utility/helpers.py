from datetime import timedelta
import arrow
import datetime
import logging

logger = logging.getLogger('IdleBot Logger')


def calculate_average_idle_time():
    pass


# measures the amount of idle time between now and then (the given timestamp, which should be user's last message or
# last active in voice comms.

def check_idle_time(ts: datetime.datetime):

    current_time = arrow.now('US/Central').datetime
    difference = current_time - ts
    duration_in_seconds = difference.total_seconds()
    days = timedelta(seconds = duration_in_seconds).days
    remaining_seconds = timedelta(seconds = duration_in_seconds).seconds
    hours = remaining_seconds // 3600
    minutes = (remaining_seconds // 60) % 60
    time_idle = { 'days': days, 'hours': hours, 'minutes': minutes }

    return time_idle

