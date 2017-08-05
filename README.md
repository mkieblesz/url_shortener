# URL Shortener

Simple flask application for url shortening.

## Guidelines

### Development

Make sure you have `virtualenv` installed. Run `make setup-dev` to setup development environment.

### Devops

It is planned that the app will use redis cluster as a store service. In order to configure app properly developer
should provide config file which should be created using provisioning tools.

In order to run test suit on a CI server run `make ci_test`.

## TODO

- register json response exceptions - perform appropriate validatation on the url to be shortened, and return appropriate error responses if the url is not valid
- You should also build your webservice in a way that a devops enginer (or you) could configure your backend in a way that your webservice could handle high traffic (eg. 1000 rps). Please explain in your `README.md` file how to configure your backend for scale.
- create docker instance with instance based configuration for integration testing
