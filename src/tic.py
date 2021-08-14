import time

from redis import Redis

import settings

redis = Redis(host=settings.REDIS_HOST,
              port=settings.REDIS_PORT,
              decode_responses=True)

while True:
    print('.')
    time.sleep(1)
    redis.incr('counter')
