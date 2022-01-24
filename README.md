# laa-court-data-api
LAA Court Data API layer to serve data from LAA Court Data Adaptor to LAA Court Data UI

Information around this service can be found within the [runbook](https://dsdmoj.atlassian.net/wiki/spaces/AAC/pages/3840311923/Court+Data+API+Runbook)

## Setting up the service

This application is using python 3.10.

### Installing venv

This application uses venv for its virtual environment. To get started run the following commands
```shell
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```

### Running the application

Running the application can be done by using the following command from the root of the project
```shell
python ./laa-court-data-api-app/main.py --reload
```
The application will reload on code changes to save on rebuild times

### Running tests

Running tests can be done by using the following command from the root of the project
```shell
pytest
```
