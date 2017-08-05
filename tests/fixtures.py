import pytest

from flask_redis import FlaskRedis

from url_shortener.application import get_test_app


@pytest.yield_fixture
def app():
    a = get_test_app()
    a.testing = True

    a.store.redis._redis_client.flushall()

    with a.app_context():
        yield a
