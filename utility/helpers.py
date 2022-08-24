# Standard packages
import datetime
import logging
from datetime import timedelta
from time import perf_counter_ns

# Third party packages
import arrow


def calculate_average_idle_time() -> int:
    pass


# measures the amount of idle time between now and then (the given timestamp, which should be user's last message or
# last active in voice comms.


def check_idle_time(ts: datetime.datetime) -> dict:
    logging.info("Calculating idle time...")
    func_start: int = perf_counter_ns()
    current_time = arrow.now("US/Central").datetime
    difference = current_time - ts
    duration_in_seconds = difference.total_seconds()
    days = timedelta(seconds=duration_in_seconds).days
    remaining_seconds = timedelta(seconds=duration_in_seconds).seconds
    hours = remaining_seconds // 3600
    minutes = (remaining_seconds // 60) % 60
    time_idle = {"days": days, "hours": hours, "minutes": minutes}
    func_end: int = perf_counter_ns()
    time_to_complete: float = (func_end - func_start) / 1000
    logging.info(
        f"Operation finished in {time_to_complete} ms\n-------------------------"
    )

    return time_idle
