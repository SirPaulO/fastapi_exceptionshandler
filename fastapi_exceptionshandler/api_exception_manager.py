from fastapi.exceptions import RequestValidationError
from .api_exception import APIException
from .api_exception_handler import APIExceptionHandler
from fastapi_routesmanager import RouteManager
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import Response
from typing import Callable, List, Type, Optional


class APIExceptionManager(RouteManager):

    def __init__(self, capture_unhandled: bool = True, capture_validation=False):
        self.capture_unhandled = capture_unhandled
        self.capture_validation = capture_validation

    async def run(
            self,
            request: Request,
            call_next: Callable,
            remaining_managers: List[Type[RouteManager]],
    ) -> Optional[Response]:
        try:
            response: Response = await call_next(request, remaining_managers)
        except APIException as exc:
            return await APIExceptionHandler.handled(exc)
        except Exception as exc:
            if type(exc) in [RequestValidationError, ValidationError] and not self.capture_validation:
                raise
            if not self.capture_unhandled:
                raise
            return await APIExceptionHandler.unhandled(exc)
        return response
