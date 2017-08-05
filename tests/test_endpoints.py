import json
import requests_mock

from fixtures import app

TEST_URL = 'http://www.google.co.uk'


def test_shorten_url(app):
    client = app.test_client()

    body = json.dumps({'url': TEST_URL})
    res = client.put('/shorten_url', data=body, content_type='application/json')

    assert res.status_code == 201
    assert json.loads(res.data)['shortened_url'].startswith(app.config['SERVICE_URL'])


def test_shorten_url_validator(app):
    client = app.test_client()

    # bad url format
    body = json.dumps({'url': 'bad url'})
    res = client.put('/shorten_url', data=body, content_type='application/json')
    assert res.status_code == 400
    assert json.loads(res.data) == {'error': {'message': 'Provided url is not valid'}}

    # no url in body
    body = json.dumps({'badparam': TEST_URL})
    res = client.put('/shorten_url', data=body, content_type='application/json')
    assert res.status_code == 400
    assert json.loads(res.data) == {'error': {'message': 'Url was not provided'}}

    # no a json request
    body = json.dumps({'url': TEST_URL})
    res = client.put('/shorten_url', data=body)
    assert res.status_code == 415
    assert json.loads(res.data) == {'error': {'message': 'Unsupported request format'}}


def test_lookup_url_redirect(app):
    client = app.test_client()

    code = 'xxx'
    app.store.set('xxx', TEST_URL)

    res = client.get('%s' % code)

    assert res.status_code == 302


def test_lookup_url_forward(app):
    client = app.test_client()

    code = 'xxx'
    app.store.set('xxx', TEST_URL)

    with requests_mock.mock() as m:
        m.get(TEST_URL, text='test_url_response')

        res = client.get('%s?forward' % code)

    assert res.status_code == 200
    assert res.data == 'test_url_response'


def test_lookup_url_404(app):
    client = app.test_client()

    res = client.get('notexistingcode')

    assert res.status_code == 404
