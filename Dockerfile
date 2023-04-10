FROM python:3.10.10-slim-bullseye

LABEL maintainer="danil.zlatoust9999@gmail.com"

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

RUN echo deb http://deb.debian.org/debian bullseye contrib non-free > /etc/apt/sources.list.d/debian-contrib.list \
  && apt update \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

ADD requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /src
ADD src /src

ARG RELEASE=dev-untagged

USER root

CMD python main.py
