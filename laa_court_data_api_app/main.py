import logging

import uvicorn
from fastapi import FastAPI
from .routers import ping, defendant

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(ping.router)
app.include_router(defendant.router)


@app.get('/')
async def root():
    logger.debug('Calling GET Endpoint')
    return {'Status': 'Working'}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
