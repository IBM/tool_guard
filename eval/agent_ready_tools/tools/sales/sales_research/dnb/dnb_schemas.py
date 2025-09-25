from typing import Any

from pydantic.dataclasses import dataclass


@dataclass
class ErrorResponse:
    """Represent the Error Response in Dun and Bradstreet API."""

    message: Any
    payload: Any
    status_code: int
