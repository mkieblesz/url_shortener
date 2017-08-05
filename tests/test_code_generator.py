from url_shortener.generator import code_generator
from fixtures import app

TEST_URL = 'http://www.google.co.uk'


def test_code_generator(app):

    code = code_generator(TEST_URL)
    assert len(code) == app.config['CODE_LENGTH']

    # same url will give same code each time
    assert code == code_generator(TEST_URL)


def test_code_generator_collisions(app):
    app.config['CODE_LENGTH'] = 3

    code = code_generator(TEST_URL)
    assert len(code) == 3

    # set different url under same code
    app.store.set(code, 'http://www.example.com')
    code = code_generator(TEST_URL)
    # there was url under same code hence one character was added
    assert len(code) == 4
