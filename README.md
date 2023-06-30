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

###  Docker configuration
- First docker configuration for local development
- File: docker-compose.yml
- Run the following command:
- Ports used (80, 5432, 8000), _Check port availability on local PC_
```bash
docker compose -f docker-compose.yml up --build
```

- Get containers id in another terminal window (IMAGE name - like: _momspops-api-backend_)
```bash
docker ps 
```

- !!! Run test
```bash
 docker exec -it <container_id> python manage.py test
 ```
- Create superuser 
```bash
 docker exec -it <container_id> python manage.py createsuperuser
 ```
 - Check in project browser:
 _http://localhost/admin/_
 _http://localhost/api/v1/_
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
SECRET_KEY=secret_SECRET
DEBUG=True

DB_NAME=postgres
DB_HOST=db
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=password
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


## Database schema
https://lucid.app/lucidchart/736ac949-7e84-4be3-96b2-25e91ec53ec8/edit?beaconFlowId=C39989B530A6D57F&invitationId=inv_c894ff77-5e97-4e8d-823f-0ffeb53dc3c7&page=0_0#
