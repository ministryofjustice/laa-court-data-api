import uvicorn
from config.app import AppSettings, get_app_settings
from fastapi import FastAPI, Depends

app = FastAPI()


@app.get("/")
async def root(settings: AppSettings = Depends(get_app_settings)):
    return {
        "Status": "Working",
        "App_Name": settings.app_name
    }

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
