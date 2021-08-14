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
