## Local development with Python, Docker and PyCharm.

In the another (post)[https://gonzalo123.com/2021/08/02/handling-m1-problems-in-python-local-development-using-docker/.] we spoke about how to handle M1 problems in Python using Docker for local development. It works like a charm but sometimes we can face problems. For example. Imagine a little more complex scenario than the previous post one. 

Now we have a Flask api that shows a value taken from a Redis database. And another process that increments this value each second. 

That's the process that updates the value within Redis:

```python
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
```

And our API:

```python
from flask import Flask
from flask import jsonify
from redis import Redis

import settings

redis = Redis(host=settings.REDIS_HOST,
              port=settings.REDIS_PORT,
              decode_responses=True)

app = Flask(__name__)


@app.route("/")
def hello_world():
    return jsonify(dict(
        name='Gonzalo',
        counter=redis.get('counter')
    ))
```

This project needs a redis server. We can run a redis server in our host. I like to use a docker-compose file to set up my extra servers. In this case 'docker-compose-servers.yml'

````yaml
version: '3.6'

services:
  redis:
    image: redis:latest
    ports:
      - 6379:6379
````

running this docker-compose file we set up a Redis server at localhost. The "problem" is that we need to access to this port from our containers and the localhost in our container is not the same localhost as our host's one. We can use our host's ip instead of localhost. I don't like to do that. Sometimes I'm in a VPN, sometimes in my housse, sometimes at office, ... and the ip changes. 

Docker allows us to handle this problem. We only need to add this parameter when we run docker

```
--add-host=host.docker.internal:host-gateway
```

If we're using PyCharm (my case) in Run/debug application > Configuration > Docker container settings > Run options

Now instead of localhost we need to use "host.docker.internal". That's all