import datetime
import time
import os
import json
import tempfile
import uuid
from .packages import six
#----------------------------------------------------------------------
def create_uid():
    if six.PY2:
        return uuid.uuid4().get_hex()
    else:
        return uuid.uuid4().hex
#----------------------------------------------------------------------
def _date_handler(obj):
    if isinstance(obj, datetime.datetime):
        return local_time_to_online(obj)
    else:
        return obj
#----------------------------------------------------------------------
def local_time_to_online(dt=None):
    """
       converts datetime object to a UTC timestamp for AGOL
       Inputs:
          dt - datetime object
       Output:
          Long value
    """
    if dt is None:
        dt = datetime.datetime.now()

    is_dst = time.daylight and time.localtime().tm_isdst > 0
    utc_offset =  (time.altzone if is_dst else time.timezone)

    return (time.mktime(dt.timetuple())  * 1000) + (utc_offset *1000)
#----------------------------------------------------------------------
def online_time_to_string(value,timeFormat):
    """
       Converts a timestamp to date/time string
       Inputs:
          value - timestamp as long
          timeFormat - output date/time format
       Output:
          string
    """
    return datetime.datetime.fromtimestamp(value /1000).strftime(timeFormat)
#----------------------------------------------------------------------
def timestamp_to_datetime(timestamp):
    """
       Converts a timestamp to a datetime object
       Inputs:
          timestamp - timestamp value as Long
       output:
          datetime object
    """
    return datetime.datetime.fromtimestamp(timestamp /1000)