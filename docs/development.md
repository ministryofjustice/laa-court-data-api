# Development

## Config
Configuration for the app is stored within the /laa_court_data_api_app/config/ directory of the repository

[Read here](https://fastapi.tiangolo.com/advanced/settings/#the-env-file) for more information about how settings work in FastAPI. Note that config should be added as a dependency to a given module as such: 

`from laa_court_data_api_app.config.settingsFile import targetSetting, targetSettingFunc`


Where targetSetting is a defined class for the config and targetSettingFunc is an instantiation function for the class.

Note that the settings are cached once instantiated, if you need to change settings whilst the app is running e.g. during unit tests, you need to run `clear_cache()` on the function that gets the settings before any extra processes

The purpose of each of the config files is as follows:

| Filename  | Purpose             |
|-----------|---------------------|
| app.py    | Global app settings |

.env file environment variables are included in the app settings via [the Pydantic in-built support for dotenv](https://fastapi.tiangolo.com/advanced/settings/#the-env-file)

Settings: 

| Variable   | Purpose                                                  | Optional                          |
|------------|----------------------------------------------------------|-----------------------------------|
| APP_NAME   | An identifier for the app                                | No (Defaults to "Court Data API") |
 | COMMIT_ID  | ID of the commit that the target version of the app is linked to | Yes                               |   
 | BUILD_DATE | Date the app was built via build tools                   | Yes                               |
| BUILD_TAG  | Tag       of the target version of the app              | Yes                               |
| APP_BRANCH | Name of branch that the target version of the app is linked to | Yes                               |
