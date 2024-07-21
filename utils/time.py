import time
import datetime

def now():
    now = datetime.datetime.now()
    return now

def timestamp(datetime = datetime.datetime.now):
    timestamp = time.mktime(datetime.timetuple())
    return timestamp
