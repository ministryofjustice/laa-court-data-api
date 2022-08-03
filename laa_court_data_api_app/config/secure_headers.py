import json
import typing
import secure

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp
from starlette.requests import Request
from starlette.responses import Response

referrer = secure.ReferrerPolicy().no_referrer()
cache_control = secure.CacheControl().no_store()
x_frame_options = secure.XFrameOptions().sameorigin()
hsts = secure.StrictTransportSecurity().include_subdomains().preload().max_age(2592000)
csp = (
    secure.ContentSecurityPolicy()
    .default_src("'self'")
    .base_uri("'self'")
    .img_src("'self'", "fastapi.tiangolo.com", "data:")
    .style_src("'self'", "cdn.jsdelivr.net", "'unsafe-inline'")
    .script_src("'self'", "cdn.jsdelivr.net", "'unsafe-inline'")
)

secure_headers = secure.Secure(
    referrer=referrer,
    cache=cache_control,
    xfo=x_frame_options,
    hsts=hsts,
    csp=csp
    )


class SecureHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        secure_headers.framework.fastapi(response)
        return response

class SecureJsonResponse(Response):
    media_type = "application/json; charset=utf-8"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")
