from abc import ABC
from enum import Enum
from typing import Optional


class APIException(ABC, Exception):
    status_code = 500

    class ErrorCode(Enum):
        InternalError = "Internal Server Error"

    def __init__(self, error_code: Enum = ErrorCode.InternalError, exc: Exception = None) -> None:
        self._error_code = error_code
        self._exc = exc

    def __str__(self) -> str:
        return self._error_code.value

    def get_error_code(self) -> str:
        return self._error_code.name

    def get_exception(self) -> Optional[Exception]:
        return self._exc

    @classmethod
    def get_status_code(cls) -> int:
        return cls.status_code


class APIError(APIException):
    status_code = 400
