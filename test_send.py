import time
from db.controller import MysqlDB, RedisDB, RedisMQ
from utils.time import now, timestamp

mq = RedisMQ()

now = now()
print({'event': '자해', 'location': '유치장1', 'occurred_at': timestamp(now)})
# mq.send('event', {'event': '자해', 'location': '유치장1', 'occurred_at': now})