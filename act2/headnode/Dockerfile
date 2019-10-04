FROM ubuntu:latest

WORKDIR /headnode/

EXPOSE 5000

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
	&& apt-get -y install python3

COPY headnode.py /headnode/
