# laa-court-data-api

## THIS REPOSITORY HAS BEEN RETIRED
This API was a proxy between laa-view-court-data and laa-court-data-adaptor. It had very little functionality, and, being written in a different language with different frameworks to the other repositories in the same system, made the system harder to maintain, harder to reason about, less reliable, more expensive and less performant. laa-view-court-data now talks directly to laa-court-data-adaptor and this codebase is no longer used.

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ministryofjustice_laa-court-data-api&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ministryofjustice_laa-court-data-api)

LAA Court Data API layer to serve data from LAA Court Data Adaptor to LAA Court Data UI

Information around this service can be found within the [runbook](https://dsdmoj.atlassian.net/wiki/spaces/AAC/pages/3840311923/Court+Data+API+Runbook)

## Setting up the service

This application is using python 3.10

### Installing pipenv

This application uses pipenv for its virtual environment. To get started run the following commands
```shell
$ pip3 install pipenv
$ pipenv shell
$ pipenv install --dev
```

### Running the application

Running the application can be done by using the following command from the root of the project
```shell
uvicorn laa_court_data_api_app.main:app --reload
```
The application will reload on code changes to save on rebuild times

### Running locally with Docker

To run via a docker container:
1. Perform the docker build with: 

`docker-compose build app`
2. You can optionally set build arguments by adding:

`--build-arg arg_name='arg_value'`
4. Run the container with:

`docker-compose up app`


### Running tests

Unit tests
Run units tests with the following command from the root of the project
```shell
pytest --cov-report term --cov=laa_court_data_api_app test
```

API tests
API tests are grouped into collections. Run each collection with the following command
```shell
newman run [collection_file] -e postman/environments/local.postman_environment.json
```


### Running linters

Running linters can be done using the following command from the root of the project
```shell
pycodestyle .
```


## Documentation
* [Development](docs/development.md)

