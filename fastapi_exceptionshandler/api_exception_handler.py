import logging
import os
from typing import Any, Dict, Optional

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from .api_exception import APIException


class APIExceptionHandler:
    error_label = "errorCode"
    message_label = "message"

    @classmethod
    def handled(
        cls, request: Request, exc: APIException, body_extra: Optional[Dict] = None, **kwargs: Any
    ) -> JSONResponse:
        body_content = {
            cls.error_label: exc.get_error_code(),
            cls.message_label: str(exc),
        }
        if body_extra is not None:
            body_content = {**body_content, **body_extra}

        # Append "exc" to the response for DEBUG purposes
        if str(os.environ.get("DEBUG", False)) == "True" and exc.get_exception() is not None:
            body_content["exc"] = str(exc.get_exception())

        return JSONResponse(status_code=exc.status_code, content=body_content, **kwargs)

    @classmethod
    def unhandled(
        cls, request: Request, exc: Exception, body_extra: Optional[Dict] = None, **kwargs: Any
    ) -> JSONResponse:
        api_exc = APIException(exc=exc)
        return cls.handled(request, api_exc, body_extra, **kwargs)

    @classmethod
    def handle_exception(
        cls,
        request: Request,
        exc: Exception,
        capture_unhandled: bool = True,
        capture_validation: bool = False,
        log_error: bool = True,
        logger_name: str = "app.exception_handler",
    ) -> JSONResponse:
        logger = logging.getLogger(logger_name) if log_error else None

        if issubclass(type(exc), APIException):
            if log_error:
                logger.error(str(exc))
            return APIExceptionHandler.handled(request, exc)  # type: ignore

        if log_error:
            logger.error(str(exc))

        if issubclass(type(exc), (RequestValidationError, ValidationError)) and not capture_validation:
            raise

        if not capture_unhandled:
            raise

        return APIExceptionHandler.unhandled(request, exc)
