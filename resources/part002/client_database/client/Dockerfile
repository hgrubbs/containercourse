#FROM python:3.9.5-buster
FROM pypy:3-7
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
WORKDIR /client
