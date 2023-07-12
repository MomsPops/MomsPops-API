# MomsPops API
[![Build Status](https://github.com/MomsPops/MomsPops-API/actions/workflows/django.yml/badge.svg)](https://github.com/MomsPops/MomsPops-API/actions/workflows/django.yml/)

# Work branch - development
## For developers:

#### Аgreements:
- default .env file: .dev.env (in ./src);
- default database: Postgres;
- default requirements file: "requirements.txt";
- unit tests folders: "tests" folder in each app with "test_model.py" and "test_view.py";
- model managers: custom manager should be extra attributes;
You can change it in settings.

#### Applications:
- _core_: project root app;
- _api_: api application;

- users
- coordinates
- locations
- notifications
- profiles
- chat
- reactions

#### Important Files and Folders:
- _service_: abstract_models, vk_api
- _.flake8_: linter settings
- _mypy.ini_: settings for checking typing configuration


#### Environ variables example:
".dev.env" file in ./src:
```dotenv
# Django settings
SECRET_KEY=secret_SECRET

# Database settings
DB_NAME=mosmpops.sqlite3
DB_HOST=localhost
DB_PORT=5432
DB_USER=admin
DB_PASSWORD=password

# Services keys
OPENCAGE_API_KET=b8fcasdasd228862e4ee9b8efd5817fac44ea
GOOGLE_MAPS_API_KEY=AIzaSyDU48asgfasf3kKemLgrFn78M1Rd_kV9kTH34XvA

# redis settings
REDIS_HOST=redis
REDIS_PORT=6379

# Emailing settings
EMAIL_HOST=smtp.gmail.com
EMAIL_FROM=suslanchikmop123l@gmail.com
EMAIL_HOST_USER=suslanchikmop123l@gmail.com
EMAIL_HOST_PASSWORD=pbkkmpsbfkhpyimz
EMAIL_PORT=587
EMAIL_USE_TLS=True

PASSWORD_RESET_TIMEOUT=14400

```
#### Linter:

We use `flake8`.
```commandline
flake8
```

#### Type-checker:

We use `mypy`
```commandline
mypy .
```

#### PRs:
IMPORTANT! You should check your code by linter and type-checker before making pull-request.

## Running application
Application is running using `Docker`. Install and activate WSL2 if you user Windows (https://docs.docker.com/desktop/wsl/).

```commandline
docker-compose up
```

## Database schema
https://lucid.app/lucidchart/736ac949-7e84-4be3-96b2-25e91ec53ec8/edit?beaconFlowId=C39989B530A6D57F&invitationId=inv_c894ff77-5e97-4e8d-823f-0ffeb53dc3c7&page=0_0#
