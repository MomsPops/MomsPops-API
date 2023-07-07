FROM python:3.11

COPY docker-requirements2.txt ./docker-requirements2.txt
COPY src ./src

WORKDIR ./src
EXPOSE 8000

RUN pip install -U -r /docker-requirements2.txt

RUN adduser --disabled-password core-user

USER core-user
