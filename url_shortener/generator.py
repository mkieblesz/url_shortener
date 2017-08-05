import base64
import hashlib
import random
import string

from flask import current_app

MAX_COLLISION_LENGTH = 4


def code_generator(url):
    '''Generate code from url

    Function returns code with length specified in config. With same url function will return same code each time.
    Simple mechanism is implemented to handle collisions for shorter codes.
    '''
    code_length = current_app.config['CODE_LENGTH']

    # create hash for providede url
    m = hashlib.sha256()
    m.update(url)

    url_digest = m.digest()

    # encode digest and make sure it contains only alphanumeric characters
    code = base64.b64encode(url_digest).replace('/', 'b').replace('+', 'c').replace('=', 'a')[:code_length]

    current_url = current_app.store.get(code)

    if code_length < MAX_COLLISION_LENGTH:
        # look for unique code
        while True:
            if not current_url or current_url == url:
                break

            code += random.choice(string.letters + string.digits)
            # code[random.randint(1, 8)] = random.choice(string.letters + string.digits)

            current_url = current_app.store.get(code)

    if not current_url:
        current_app.store.set(code, url)

    return code
