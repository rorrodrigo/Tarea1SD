FROM ubuntu:latest

WORKDIR /datanode3/

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
	&& apt-get -y install python3

COPY datanode3.py /datanode3/
