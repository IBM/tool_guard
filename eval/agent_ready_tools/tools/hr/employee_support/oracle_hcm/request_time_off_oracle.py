from enum import Enum
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS

TIME_OFF_SUBMIT_STATUS: str = "SUBMITTED"


class AbsenceDuration(Enum):
    """Enum for absence durations."""

    HALF_DAY = "0.5"
    FULL_DAY = "1"


@dataclass
class RequestTimeOffResponse:
    """Response after requesting time off in Oracle HCM."""

    absence_request_id: int
    status: str
    absence_type: str
    employer: str
    start_date: str
    end_date: str
    formatted_duration: str


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def request_time_off_oracle(
    person_id: str,
    employer_id: int,
    absence_type_name: str,
    start_date: str,
    end_date: str,
    start_time: str,
    end_time: str,
    duration: Optional[str] = None,
    absence_reason: Optional[str] = None,
) -> RequestTimeOffResponse:
    """
    Submits a time off request for a user in Oracle HCM.

    Args:
        person_id: The person_id uniquely identifying them within the Oracle HCM returned by the
            `get_user_oracle_ids` tool.
        employer_id: The ID of the employer or legal entity, returned by the `get_absence_types`
            tool.
        absence_type_name: The name of the absence type, returned by the `get_absence_types` tool.
        start_date: The start date of the requested time off in ISO 8601 format (YYYY-MM-DD).
        end_date: The end date of the requested time off in ISO 8601 format (YYYY-MM-DD).
        start_time: Start time of absence in HH:MM format (24-hour clock).
        end_time: End time of absence in HH:MM format (24-hour clock).
        duration: absence duration for both start and end dates; accepted values are 0.5 and 1,
            required if the unit of measure is 'Calendar Days'.
        absence_reason: The reason for the absence, returned by the `get_absence_reasons` tool.
            Required if any absence reasons associated with absence type .

    Returns:
        The result from performing the request time off.
    """

    durations = [duration.value for duration in AbsenceDuration]
    if duration and duration not in durations:
        raise ValueError(
            f"duration '{duration}' is not a valid value. Accepted values are {durations}"
        )

    client = get_oracle_hcm_client()

    payload = {
        "personId": person_id,
        "absenceType": absence_type_name,
        "legalEntityId": employer_id,
        "startDate": start_date,
        "endDate": end_date,
        "startTime": start_time,
        "endTime": end_time,
        "startDateDuration": duration if duration else None,
        "endDateDuration": duration if duration else None,
        "absenceStatusCd": TIME_OFF_SUBMIT_STATUS,
        "absenceReason": absence_reason,
    }

    payload = {key: value for key, value in payload.items() if value}

    response = client.post_request(entity="absences", payload=payload)

    return RequestTimeOffResponse(
        absence_request_id=response["personAbsenceEntryId"],
        status=response["approvalStatusCd"],
        absence_type=response["absenceType"],
        employer=response["employer"],
        start_date=response["startDate"],
        end_date=response["endDate"],
        formatted_duration=response["formattedDuration"],
    )
