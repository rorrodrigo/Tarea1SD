FROM ubuntu:latest

WORKDIR /datanode2/

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
	&& apt-get -y install python3

COPY datanode2.py /datanode2/
