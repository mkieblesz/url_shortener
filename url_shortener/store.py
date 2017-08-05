import json
import os


class Store():
    def get(self, code):
        raise NotImplementedError()

    def set(self, code, url):
        raise NotImplementedError()


class FileStore(Store):
    def __init__(self, filename='store.json'):
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                f.write('{}')

    def get(self, code):
        with open(self.filename, 'r') as f:
            return json.load(f).get(code, None)

    def set(self, code, url):
        with open(self.filename, 'r') as f:
            data = json.load(f)

        data[code] = url

        with open(self.filename, 'w') as f:
            json.dump(data, f)


class RedisStore(Store):
    def __init__(self, redis_client, prefix='store:'):
        self.redis = redis_client
        self.prefix = prefix

    def get(self, code):
        return self.redis.get(self.prefix + code)

    def set(self, code, url):
        self.redis.set(self.prefix + code, url)
