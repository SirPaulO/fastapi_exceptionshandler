from abc import ABC
from dataclasses import dataclass, field
from enum import Enum

REPORT_LEVEL = Enum("ReportLevel", ["REPORT", "IGNORE"])


@dataclass
class ErrorCodeMixin:
    message: str
    status_code: int | None = field(default=None)
    report_level: REPORT_LEVEL | None = field(default=None)
    ignore_handler: bool = field(default=False)

    @property
    def value(self) -> str:
        return self.message


@dataclass
class ProxyErrorCode(ErrorCodeMixin):
    name: str = field(default="ProxyError")


# Base class to be extended
class ErrorCodeBase(ErrorCodeMixin, Enum):
    pass


class APIException(ABC, Exception):
    # Defaults
    status_code: int = 500
    report_level: REPORT_LEVEL = REPORT_LEVEL.IGNORE
    ignore_handler: bool = False

    # Mapped error codes with their messages, status code and report level
    class ErrorCode(ErrorCodeBase):
        InternalError = "Internal Server Error", 500, REPORT_LEVEL.IGNORE, False

    def __init__(
        self,
        error_code: ErrorCodeBase | ProxyErrorCode = ErrorCode.InternalError,
        exc: Exception | None = None,
    ) -> None:
        # Check not None status_code
        if getattr(error_code, "status_code", None) is None:
            error_code.status_code = self.status_code

        # Check not None report_level
        if getattr(error_code, "report_level", None) is None:
            error_code.report_level = self.report_level

        # Check not None ignore_handler
        if getattr(error_code, "ignore_handler", None) is None:
            error_code.ignore_handler = self.ignore_handler

        self._error_code = error_code
        self.status_code = error_code.status_code
        self.report_level = error_code.report_level
        self.ignore_handler = error_code.ignore_handler
        self._exc = exc

    def __str__(self) -> str:
        return str(self._error_code.message) if hasattr(self._error_code, "message") else str(self._error_code.value)

    def get_error_code(self) -> str:
        return str(self._error_code.name)

    def get_exception(self) -> Exception | None:
        return self._exc

    def get_status_code(self) -> int:
        return int(self._error_code.status_code) if hasattr(self._error_code, "status_code") else self.status_code

    def get_report_level(self) -> REPORT_LEVEL:
        return self._error_code.report_level if hasattr(self._error_code, "report_level") else self.report_level

    def should_report(self) -> bool:
        return self.get_report_level() == REPORT_LEVEL.REPORT

    def should_ignore_handler(self) -> bool:
        return self.ignore_handler


class APIError(APIException):
    status_code = 400
