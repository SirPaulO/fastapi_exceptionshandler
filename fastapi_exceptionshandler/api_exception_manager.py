from typing import Callable, List, Optional, Type

from fastapi_routesmanager import RouteManager
from starlette.requests import Request
from starlette.responses import Response

from . import APIExceptionHandler


class APIExceptionManager(RouteManager):
    def __init__(
        self,
        capture_unhandled: bool = True,
        capture_validation: bool = False,
        logger_name: Optional[str] = None,
        log_error: bool = True,
    ):
        self.capture_unhandled = capture_unhandled
        self.capture_validation = capture_validation
        self.logger_name = logger_name
        self.log_error = log_error

    async def run(
        self,
        request: Request,
        call_next: Callable,
        remaining_managers: List[Type[RouteManager]],
    ) -> Optional[Response]:
        try:
            response = await call_next(request, remaining_managers)
        except Exception as exc:
            return APIExceptionHandler.handle_exception(
                request,
                exc,
                capture_unhandled=self.capture_unhandled,
                capture_validation=self.capture_validation,
                logger_name=self.logger_name,
                log_error=self.log_error,
            )
        return response
