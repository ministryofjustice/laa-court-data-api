# laa-court-data-api
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
python ./laa_court_data_api_app/main.py --reload
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

Running tests can be done by using the following command from the root of the project
```shell
pytest --cov-report term --cov=laa_court_data_api_app test
```

## Documentation
* [Development](docs/development.md)

### Running linters

Running linters can be done using the following command from the root of the project
```shell
pycodestyle .
```