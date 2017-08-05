import requests
import validators

from flask import current_app, request, abort, jsonify, redirect

from url_shortener.exceptions import UrlValidationException, BadRequestFormatException, NotFoundException
from url_shortener.generator import code_generator


def lookup_url(code):
    url = current_app.store.get(code)

    if not url:
        raise NotFoundException(404)

    if 'forward' in request.args:
        return requests.get(url).text

    return redirect(url)


def shorten_url():
    if not request.is_json:
        raise BadRequestFormatException()

    data = request.get_json()
    if 'url' not in data:
        raise UrlValidationException(msg='Url was not provided')

    url = data['url'].strip()
    if not validators.url(url):
        raise UrlValidationException()

    code = code_generator(url)

    response = jsonify({
        'shortened_url': current_app.config['SERVICE_URL'] + '/' + code
    })
    response.status_code = 201
    return response
