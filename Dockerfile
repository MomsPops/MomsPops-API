FROM python:3.11

COPY docker-requirements.txt ./docker-requirements.txt
COPY src ./src

WORKDIR ./src
EXPOSE 8000

RUN pip install -U -r /docker-requirements.txt

RUN adduser --disabled-password core-user

USER core-user
