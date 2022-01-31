import uvicorn
from laa_court_data_api_app.config.app import AppSettings, get_app_settings
from fastapi import FastAPI, Depends

app = FastAPI()


@app.get("/")
async def root(settings: AppSettings = Depends(get_app_settings)):
    return {
        "Status": "Working",
        "App_Name": settings.app_name,
        "Commit_ID": settings.commit_id,
        "Build_Date": settings.build_date,
        "Build_Tag": settings.build_tag,
        "App_Branch": settings.app_branch
    }

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
