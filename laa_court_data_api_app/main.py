import logging

import uvicorn
from fastapi import FastAPI
from .routers import ping, hearing_summaries

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(ping.router)
app.include_router(hearing_summaries.router)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
