# MomsPops API
[![Build Status](https://github.com/MomsPops/MomsPops-API/actions/workflows/django.yml/badge.svg)](https://github.com/MomsPops/MomsPops-API/actions/workflows/django.yml/)
## For developers:

#### Аgreements:
- default .env file: .dev.env;
- default database: Postgres;
- default requirements file: "requirements.txt";
- unit tests folders: "tests" folder in each app with "test_model.py" and "test_view.py";
- model managers: custom manager should be extra attributes;
You can change it in settings.

#### Applications:
- core: project root app;
- api: api application;
- users: application for users; 


#### Environ variables example:
".dev.env" file:
```dotenv
SECRET_KEY=secret_SECRET

DB_NAME=mosmpops_example
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
```


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


## Database schema
https://drive.google.com/file/d/120bxgsR9spj89HfDvYM9-zAic_IlBGEc/view
