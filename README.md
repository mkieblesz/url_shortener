# URL Shortener

Simple flask application for url shortening.

## Guidelines

### Installation

Make sure you have `virtualenv` installed. Run `make setup-dev` to setup development environment.

To run performance tests agains docker container run `make docker-all`. This will setup docker on your machine, build container, run it and finally run performance tests using Taurus.

This application was developed on Ubuntu 14.04, so you might have problems when running it on different OS.

### Development

For local testing use `make test` command. To run local development server execute `make run-server`.

### Devops

It is planned that the app will use redis cluster as a store service. In order to configure app properly developer
should provide config file which should be created using provisioning tools in `url_shortener/config.cfg`.

In order to run test suit on a CI server run `make ci_test`.

To achieve higher performance please find best pair of threads and workers for machine application is deployed on. You
can find this configuration in `server/supervisor.conf`. To make local tests use running docker image with `make docker-taurus-test`.

### TODO

- for development run redis in different container and use docker compose for linking
- write performance test for 1000rps on lookup_url endpoint
- use docker taurus image to run performance tests
- config.cfg should be set in dockerfile, because currently response doesn't have correct service url
