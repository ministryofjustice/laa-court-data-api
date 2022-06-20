import logging
import structlog
from structlog.stdlib import LoggerFactory

import sentry_sdk
import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.context import correlation_id
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.httpx import HttpxIntegration
from starlette.responses import RedirectResponse
from starlette_prometheus import PrometheusMiddleware, metrics
from typing import Any

from laa_court_data_api_app.config import logging_config
from laa_court_data_api_app.config.app import get_app_settings
from .routers import defendants, hearing, hearing_summaries, hearing_events, laa_references, ping


def add_correlation(
        logger: logging.Logger, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Add request id to log message."""
    if request_id := correlation_id.get():
        event_dict["request_id"] = request_id
    return event_dict


def capture_event(event):
    return event


structlog.configure(logger_factory=LoggerFactory(), processors=[
    add_correlation,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M.%S"),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    structlog.processors.JSONRenderer()
], wrapper_class=structlog.stdlib.BoundLogger,
                    cache_logger_on_first_use=True)
logging.config.dictConfig(logging_config.config)

sentry_sdk.init(dsn=get_app_settings().sentry_dsn,
                release=get_app_settings().build_tag,
                sample_rate=1.0,
                traces_sample_rate=0.1,
                integrations=[
                    HttpxIntegration()
                ],
                before_send=capture_event)

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
