#!/bin/bash

cd src
python3 manage.py collectstatic --no-input
python3 manage.py makemigrations
python3 manage.py migrate --no-input
gunicorn core.wsgi -b 0.0.0.0:8000
