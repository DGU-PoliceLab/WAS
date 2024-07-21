import time
from db.controller import MysqlDB, RedisDB, RedisMQ
from services import cctv, location, log
from utils.time import now_timestamp

mq = RedisMQ()

print("!!!!!!!!!!!!!!!!!!")
while True:

    if not mq.is_empty('event'):
        message = mq.recv('event')
        print(message)
    else:
        print("no message")
    time.sleep(0.1)