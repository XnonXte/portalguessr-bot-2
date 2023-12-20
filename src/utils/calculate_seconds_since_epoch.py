import math
from datetime import datetime


def calculate_seconds_since_epoch(js_datetime):
    py_datetime = datetime.fromisoformat(js_datetime[:-1])

    return math.floor((py_datetime - datetime(1970, 1, 1)).total_seconds())
