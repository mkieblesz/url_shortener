class Config(object):
    # use DEBUG mode?
    DEBUG = False

    # use TESTING mode?
    TESTING = False

    SERVICE_URL = 'http://localhost:5000'
    CODE_LENGTH = 8

    # Redis settings
    REDIS_PREFIX = 'test_url_shortener:'
    # devops team should provide redis cluster url to which we should point
    REDIS_URL = 'redis://localhost:6379/0'
    REDIS_PREFIX = 'url_shortener:'


# config class used during tests
class Test(Config):
    TESTING = True
