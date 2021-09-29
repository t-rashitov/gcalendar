FROM python:3.9.7

ENV PYTHONUNBUFFERED 1

COPY web/ /web

COPY _CI/docker-entrypoint.sh /web

WORKDIR /web

RUN chmod +x docker-entrypoint.sh

RUN pip install --upgrade pip && pip install -r requirements.txt
