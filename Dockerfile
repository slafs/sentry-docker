FROM python:2.7

MAINTAINER Sławek Ehlert <slafs@op.pl>

RUN pip install -U wheel pip setuptools

RUN apt-get -qq update && DEBIAN_FRONTEND=noninteractive apt-get install -y -q libxslt1-dev libxml2-dev libpq-dev expect

RUN mkdir -p /conf
RUN mkdir -p /data
RUN mkdir -p /wheels

ADD requirements.txt /conf/

RUN pip wheel --wheel-dir=/wheels -r /conf/requirements.txt

# the order is important because of the redis dependency (version)
RUN pip install --find-links=/wheels -r /conf/requirements.txt

EXPOSE 9000

VOLUME ["/data"]

ADD sentry.conf.py /conf/
ADD sentry_run /usr/local/bin/

ENTRYPOINT ["/usr/local/bin/sentry_run"]

CMD ["start"]
