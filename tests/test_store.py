import json
import os

from flask_redis import FlaskRedis

from url_shortener.store import FileStore, RedisStore


def test_filestore():
    store_file = '/tmp/test_store.json'

    if os.path.exists(store_file):
        os.remove(store_file)

    store = FileStore(store_file)

    assert os.path.exists(store_file)
    with open(store_file, 'r') as f:
        assert json.load(f) == {}

    store.set('foo', 'bar')

    with open(store_file, 'r') as f:
        assert json.load(f) == {'foo': 'bar'}

    assert store.get('foo') == 'bar'


def test_redisstore(app):
    redis_client = FlaskRedis(app)
    store = RedisStore(redis_client, prefix='test_store:')

    store.set('foo', 'bar')
    assert store.get('foo') == 'bar'
