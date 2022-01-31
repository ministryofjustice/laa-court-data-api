# Development

## Running

To run the app locally see [readme](../readme)

## Running locally with Docker

To run via a docker container:
1. Perform the docker build with: 

`docker-compose build app`
2. You can optionally set build arguments by adding:

`--build-arg arg_name='arg_value'`
4. Run the container with:

`docker-compose up app`


## Config
Configuration for the app is stored within the /laa_court_data_api_app/config/ directory of the repository

[Read here](https://fastapi.tiangolo.com/advanced/settings/#the-env-file) for more information about how settings work in FastAPI. Note that config should be added as a dependency to a given module as such: 

`from laa_court_data_api_app.config.settingsFile import targetSetting, targetSettingFunc
`
Where targetSetting is a defined class for the config and targetSettingFunc is an instantiation function for the class.

The purpose of each of the config files is as follows:

| Filename  | Purpose             |
|-----------|---------------------|
| app.py    | Global app settings |

.env file environment variables are included in the app settings via [the Pydantic in-built support for dotenv](https://fastapi.tiangolo.com/advanced/settings/#the-env-file)

Settings: 

| Variable   | Purpose                                                  |
|------------|----------------------------------------------------------|
| APP_NAME   | An identifier for the app                                |
 | COMMIT_ID  | ID of the commit that the target version of the app is linked to |   
 | BUILD_DATE | Date the app was built via build tools                   |
| BUILD_TAG  | Tag       of the target version of the app              |
| APP_BRANCH | Name of branch that the target version of the app is linked to |
