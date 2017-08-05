from flask import Flask
from flask_redis import FlaskRedis

from store import RedisStore
from config import Config, Test


def create_base_app():
    app = Flask(__name__)

    return app


def register_store(app):
    redis_client = FlaskRedis(app)
    app.store = RedisStore(redis_client, prefix=app.config['REDIS_PREFIX'])


def register_urls(app):
    from endpoints import shorten_url, lookup_url

    app.add_url_rule('/<code>', 'lookup_url', lookup_url, methods=['GET'])
    app.add_url_rule('/shorten_url', 'shorten_url', shorten_url, methods=['POST'])


def get_app():
    app = create_base_app()

    app.config.from_object(Config)
    app.config.from_pyfile('config.cfg', silent=True)  # instance-folders configuration

    register_store(app)
    register_urls(app)

    return app


def get_test_app():
    app = get_app()

    app.config.from_object(Test)

    return app


if __name__ == '__main__':
    get_app().run(host='0.0.0.0', port=5000)
