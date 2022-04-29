import logging

import sentry_sdk
import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.httpx import HttpxIntegration
from starlette.responses import RedirectResponse
from starlette_prometheus import PrometheusMiddleware, metrics

from laa_court_data_api_app.config import logging_config
from laa_court_data_api_app.config.app import get_app_settings
from .routers import defendants, hearing, hearing_summaries, hearing_events, laa_references, ping

logging.config.dictConfig(logging_config.config)
logger = logging.getLogger(__name__)

sentry_sdk.init(dsn=get_app_settings().sentry_dsn,
                release=get_app_settings().build_tag,
                sample_rate=1.0,
                traces_sample_rate=0.1,
                integrations=[
                    HttpxIntegration()
                ])

app = FastAPI(
    title=get_app_settings().app_name,
    version='0.0.1',
    contact={
        "name": get_app_settings().contact_team,
        "email": get_app_settings().contact_email,
        "url": get_app_settings().app_repo
    }
)

app.include_router(defendants.router)
app.include_router(hearing.router)
app.include_router(hearing_summaries.router)
app.include_router(hearing_events.router)
app.include_router(laa_references.router)
app.include_router(ping.router)

app.add_middleware(CorrelationIdMiddleware, header_name='Laa-Transaction-Id')
app.add_middleware(SentryAsgiMiddleware)
app.add_middleware(PrometheusMiddleware)

app.add_route('/metrics', metrics)


@app.get('/')
async def get_index():
    return RedirectResponse(url='/docs')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
