#FROM python:3.9.5-buster
FROM pypy:3-7
RUN mkdir /client
WORKDIR /client
COPY * /client/
RUN pip install -r /client/requirements.txt
CMD ./serve_api.sh
