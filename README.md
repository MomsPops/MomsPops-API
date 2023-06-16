# MomsPops API

For developers:

- default .env file = .dev.env
- default database - PostgreSQL

You can change it in settings.

## Installing requirements
```commandline
pip install -r requirements.txt
```

## Running application
```commandline
cd src
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
