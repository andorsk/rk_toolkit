FROM python:3.7 as intermediate
MAINTAINER Andor Kesselman <andor@henosisknot.com>

COPY requirements.txt /
WORKDIR /pip-packages/
ARG CACHEBUST=1
RUN apt-get install -y --reinstall ca-certificates
RUN git config --global url."ssh://git@github.com/".insteadOf ssh://git@github.com:
RUN pip download --no-cache-dir -r /requirements.txt

FROM mltooling/ml-workspace:0.13.2

WORKDIR /pip-packages/
LABEL maintainer="Andor <andor@henosisknot.com>"
COPY --from=intermediate /pip-packages/ /pip-packages/
RUN python -m pip install --upgrade pip
RUN apt-get install -y --reinstall ca-certificates
RUN python -m pip install --find-links=/pip-packages/ /pip-packages/*
