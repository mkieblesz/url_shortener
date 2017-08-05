ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

setup:
	virtualenv .venv
	.venv/bin/pip install -r requirements/main.txt

setup-test: setup
	.venv/bin/pip install -r requirements/test.txt

setup-dev: setup-test

run-server:
	PYTHONPATH=. .venv/bin/python url_shortener/application.py

test:
	PYTHONPATH=. .venv/bin/python -m pytest --cov url_shortener

ci-test: setup-test test

# DOCKER
docker-setup:
	sudo apt-get install --no-install-recommends linux-image-extra-virtual
	curl -o /tmp/docker.deb https://apt.dockerproject.org/repo/pool/main/d/docker-engine/docker-engine_17.05.0~ce-0~ubuntu-xenial_amd64.deb
	sudo dpkg -i /tmp/docker.deb
	rm /tmp/docker.deb
	sudo getent group docker || groupadd docker
	sudo usermod -aG docker $(USER)

	# install bzt for performance testing
	.venv/bin/pip install bzt==1.9.4

docker-build:
	docker build -t="url_shortener" .

docker-run:
	docker run -P -p 8080:80 -p 6379 -t -v $(ROOT_DIR):/opt/app url_shortener

docker-taurus-test:
	# run performance test agains docker instance
	curl -H "Content-Type: application/json" -X POST -d '{"url":"http://www.google.co.uk"}' http://localhost:8080/shorten_url
	.venv/bin/bzt tests/performance/test.yml

docker-all: docker-setup docker-build docker-run docker-taurus-test
