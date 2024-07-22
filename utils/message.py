import time
from db.controller import RedisDB, RedisMQ
from utils.time import now_timestamp

redis = RedisDB
mq = RedisMQ()

def check():
    while True:
        if not mq.is_empty('event'):
            message = mq.recv('event')
            print(message)
        else:
            print("no message")
            time.sleep(0.0001)