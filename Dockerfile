FROM ubuntu:14.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update -q && \
    DEBIAN_FRONTEND=noninteractive apt-get install -qy python-pip=1.5.4-1 \
                                                       python-dev=2.7.5-5ubuntu3 \
                                                       build-essential=11.6ubuntu6 \
                                                       && \
    apt-get clean

ENV PYTHONPATH /pymusic
WORKDIR /pymusic

COPY requirements.txt /pymusic/
RUN pip install -r /pymusic/requirements.txt

