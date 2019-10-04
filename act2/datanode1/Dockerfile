FROM ubuntu:latest

WORKDIR /datanode1/

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
	&& apt-get -y install python3
  
COPY datanode1.py /datanode1/
