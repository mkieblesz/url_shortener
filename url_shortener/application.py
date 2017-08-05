from flask import Flask, jsonify
from flask_redis import FlaskRedis

from url_shortener.store import RedisStore
from url_shortener.config import Config, Test


def create_base_app():
    app = Flask(__name__)

    return app


def register_store(app):
    redis_client = FlaskRedis(app)
    app.store = RedisStore(redis_client, prefix=app.config['REDIS_PREFIX'])


def register_urls(app):
    from endpoints import shorten_url, lookup_url

    app.add_url_rule('/<code>', 'lookup_url', lookup_url, methods=['GET'])
    app.add_url_rule('/shorten_url', 'shorten_url', shorten_url, methods=['PUT'])


def register_exceptions(app):
    from werkzeug.exceptions import HTTPException
    from url_shortener.exceptions import ErrorException, UncategorisedException

    def make_json_error(ex):
        # TODO: make more verbose error log message
        log_message = str(ex)
        if not isinstance(ex, ErrorException):
            ex = UncategorisedException(msg=log_message, status=(ex.code if isinstance(ex, HTTPException) else 500))

        if ex.is_error():
            app.logger.exception(log_message)
        else:
            app.logger.info(log_message)

        response = jsonify(ex.get_response())
        response.status_code = ex.status
        return response

    @app.errorhandler(Exception)
    def unhandled_exception(ex):
        return make_json_error(ex)

    return app


def get_app():
    app = create_base_app()

    app.config.from_object(Config)
    app.config.from_pyfile('config.cfg', silent=True)  # instance-folders configuration

    register_store(app)
    register_urls(app)
    register_exceptions(app)

    return app


def get_test_app():
    app = get_app()

    app.config.from_object(Test)

    return app


if __name__ == '__main__':
    get_app().run(host='0.0.0.0', port=5000)
