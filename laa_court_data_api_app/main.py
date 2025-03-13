import json
import logging
import structlog
from structlog.stdlib import LoggerFactory

import sentry_sdk
import uvicorn
from fastapi.exceptions import RequestValidationError
from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.context import correlation_id
from fastapi import FastAPI, Request
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.httpx import HttpxIntegration
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
from starlette_prometheus import PrometheusMiddleware, metrics
from typing import Any

from laa_court_data_api_app.config import logging_config
from laa_court_data_api_app.config.app import get_app_settings
from laa_court_data_api_app.config.secure_headers import SecureHeadersMiddleware, SecureJsonResponse
from .routers import defendants, hearings, case_summaries, hearing_events, laa_references, ping


# By default uvicorn logs requests including querystrings, which can contain PII.
# So we run uvicorn with `--no-access-log` and instead use our own logging
# here that contains the URL without the query string
class QueryStringFilterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        filtered_url = str(request.url).split("?")[0]
        logging.info(f"{request.method} {filtered_url}")

        response = await call_next(request)
        return response


def add_correlation(
        logger: logging.Logger, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Add request id to log message."""
    if request_id := correlation_id.get():
        event_dict["request_id"] = request_id
    return event_dict


# The querystring can contain PII so we don't want it in our logs
def filter_querystring(
        logger: logging.Logger, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    if "endpoint" in event_dict:
        event_dict["endpoint"] = event_dict["endpoint"].copy_with(query=b'')
    return event_dict


def send_event(event, hint):
    log_message = json.loads(event["logentry"]["message"])
    event["logentry"]["message"] = log_message["event"]
    event["logentry"]["params"] = log_message

    return event


structlog.configure(logger_factory=LoggerFactory(), processors=[
    add_correlation,
    filter_querystring,
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
                before_send=send_event)

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
app.include_router(hearings.router)
app.include_router(case_summaries.router)
app.include_router(hearing_events.router)
app.include_router(laa_references.router)
app.include_router(ping.router)

app.add_middleware(CorrelationIdMiddleware, header_name='Laa-Transaction-Id')
app.add_middleware(SentryAsgiMiddleware)
app.add_middleware(PrometheusMiddleware)
app.add_middleware(SecureHeadersMiddleware)
app.add_middleware(QueryStringFilterMiddleware)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return SecureJsonResponse(status_code=422, content=exc)

app.add_route('/metrics', metrics)


@app.get('/')
async def get_index():
    return RedirectResponse(url='/docs')


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
