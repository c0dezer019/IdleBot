from datetime import datetime, timedelta
from pytz import timezone


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
