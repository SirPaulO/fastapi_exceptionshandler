from .api_exception import APIException
from starlette.responses import JSONResponse
from typing import Any, Dict
import os


class APIExceptionHandler:
    error_label = "errorCode"
    message_label = "message"

    @classmethod
    async def handled(cls, exc: APIException, body_extra: Dict = None, **kwargs: Any) -> JSONResponse:
        body_content = {cls.error_label: exc.get_error_code(), cls.message_label: str(exc)}
        if body_extra is not None:
            body_content = {**body_content, **body_extra}

        # Append "exc" to the response for DEBUG purposes
        if str(os.environ.get("DEBUG", False)) == "True" and exc.get_exception() is not None:
            body_content["exc"] = str(exc.get_exception())

        return JSONResponse(status_code=exc.status_code, content=body_content, **kwargs)

    @classmethod
    async def unhandled(cls, exc: Exception, body_extra: Dict = None, **kwargs: Any) -> JSONResponse:
        api_exc = APIException(exc=exc)
        return await cls.handled(api_exc, body_extra, **kwargs)
