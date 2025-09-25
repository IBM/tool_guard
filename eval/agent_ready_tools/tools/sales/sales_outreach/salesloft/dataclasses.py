from enum import StrEnum
from typing import Any, Optional, Union

from pydantic.dataclasses import dataclass


class SalesloftStepType(StrEnum):
    """Possible Salesloft step types."""

    EMAIL = "email"
    PHONE = "phone"
    INTEGRATION = "integration"
    OTHER = "other"


@dataclass
class StepResponse:
    """Dataclass representing step response from Salesloft."""

    id: Optional[Union[str, int]]
    name: Optional[str]
    display_name: Optional[str]
    type: SalesloftStepType
    day: Optional[int]
    step_number: Optional[int]
    created_at: Optional[str]
    updated_at: Optional[str]
    details: Optional[str]  # map from "details" dictionary "_href" link.
    cadence_id: Optional[Union[str, int]]  # map from "cadence" dictionary "id" key value.


@dataclass
class SalesloftErrorResponse:
    """Error response from Salesloft API."""

    message: Any
