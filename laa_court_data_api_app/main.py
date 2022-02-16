import logging

import uvicorn
from fastapi import FastAPI

from laa_court_data_api_app.config.app import get_app_settings
from .routers import ping, hearing_summaries

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI(    
    title=get_app_settings().app_name,
    version='0.0.1',
    contact={
        "name": get_app_settings().contact_team,
        "email": get_app_settings().contact_email,
        "url": get_app_settings().app_repo
    }
)

app.include_router(ping.router)
app.include_router(hearing_summaries.router)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
