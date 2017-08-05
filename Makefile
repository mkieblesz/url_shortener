setup:
	virtualenv .venv
	.venv/bin/pip install -r requirements/main.txt

setup-test: setup
	.venv/bin/pip install -r requirements/test.txt

setup-dev: setup-test

runserver:
	PYTHONPATH=. .venv/bin/python url_shortener/application.py

test:
	PYTHONPATH=. .venv/bin/python -m pytest --cov url_shortener

ci_test: setup-test test
