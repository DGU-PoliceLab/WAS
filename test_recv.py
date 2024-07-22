import time
from db.controller import RedisMQ

mq = RedisMQ()

print("!!!!!!!!!!!!!!!!!!")
while True:

    if not mq.is_empty('event'):
        message = mq.recv('event')
        print(message)
    else:
        print("no message")
    time.sleep(0.1)