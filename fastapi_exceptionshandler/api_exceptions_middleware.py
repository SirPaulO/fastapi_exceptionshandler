import typing

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint
from starlette.types import ASGIApp

from . import APIExceptionHandler


class APIExceptionMiddleware(BaseHTTPMiddleware):
    """
    Middleware that catches and transforms exceptions
    """

    def __init__(
        self,
        app: ASGIApp,
        dispatch: typing.Optional[DispatchFunction] = None,
        capture_unhandled: bool = True,
        logger_name: typing.Optional[str] = None,
        log_error: bool = True,
    ):
        super().__init__(app, dispatch)
        self.capture_unhandled = capture_unhandled
        self.logger_name = logger_name
        self.log_error = log_error

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            response = await call_next(request)
        except Exception as exc:
            return APIExceptionHandler.handle_exception(
                request,
                exc,
                capture_unhandled=self.capture_unhandled,
                log_error=self.log_error,
                logger_name=self.logger_name,
            )
        return response
