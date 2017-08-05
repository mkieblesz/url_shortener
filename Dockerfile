FROM ubuntu:14.04

# keep upstart quiet
RUN dpkg-divert --local --rename --add /sbin/initctl
RUN ln -sf /bin/true /sbin/initctl

# no tty
ENV DEBIAN_FRONTEND noninteractive

# get up to date
RUN apt-get update --fix-missing

# global installs
RUN apt-get install -y build-essential git
RUN apt-get install -y python python-dev python-setuptools
RUN apt-get install -y python-pip python-virtualenv
RUN apt-get install -y nginx supervisor
RUN apt-get install -y redis-server

# create a virtual environment and install all depsendecies
RUN virtualenv /opt/venv
ADD ./requirements/main.txt /opt/venv/requirements.txt
RUN /opt/venv/bin/pip install -r /opt/venv/requirements.txt
RUN pip install supervisor-stdout

# copy config files
ADD ./server/supervisord.conf /etc/supervisord.conf
ADD ./server/nginx.conf /etc/nginx/nginx.conf

# stop services
RUN service supervisor stop
RUN service nginx stop

# restart services
CMD service redis-server restart && supervisord -c /etc/supervisord.conf -n
