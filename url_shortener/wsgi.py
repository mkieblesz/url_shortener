#!/usr/bin/python

# Usage:
# gunicorn url_shortener.wsgi --bind 127.0.0.1:5000 -w 5 --threads 5

from werkzeug.contrib.fixers import ProxyFix

from url_shortener.application import get_app

application = get_app()
application.wsgi_app = ProxyFix(application.wsgi_app)
