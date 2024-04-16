from datetime import datetime
from dateutil import tz

def convert_utc_to_local(date: datetime):
    return date.astimezone(tz.tzlocal())