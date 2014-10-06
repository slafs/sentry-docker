FROM python:2.7

MAINTAINER Sławek Ehlert <slafs@op.pl>

RUN apt-get -qq update && apt-get install -y -q netcat

RUN mkdir /tests

ADD test.sh /tests/

WORKDIR /tests

CMD ["/bin/bash", "./test.sh"]
