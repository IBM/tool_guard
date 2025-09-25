from enum import Enum
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.format_tool_input import string_to_list_of_enums
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


class TimeOffTypes(Enum):
    """Represents the time off event types in SAP SuccessFactors."""

    ABSENCE = "ABSENCE"
    PUBLIC_HOLIDAY = "PUBLIC_HOLIDAY"
    NON_WORKING_DAY = "NON_WORKING_DAY"


@dataclass
class UpcomingTimeOff:
    """Represents an upcoming time off event in SAP SuccessFactors."""

    title: str
    start_date: str
    end_date: str
    start_time: Optional[str]
    end_time: Optional[str]
    duration: int
    time_unit: str
    cross_midnight: Optional[bool]
    type: str
    status_formatted: Optional[str]
    absence_duration_category: Optional[str]


@dataclass
class UpcomingTimeOffResponse:
    """Represents the response from getting a user's upcoming time off in SAP SuccessFactors."""

    time_off_events: list[UpcomingTimeOff]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_upcoming_time_off(
    user_id: str, start_date: str, end_date: str, time_off_types: str
) -> UpcomingTimeOffResponse:
    """
    Retrieves the user's upcoming time off details from SAP SuccessFactors.

    Args:
        user_id: The user's user_id uniquely identifying them within the SuccessFactors API.
        start_date: The start of a date range filter in ISO 8601 format (e.g., YYYY-MM-DD).
        end_date: The end of a date range filter in ISO 8601 format (e.g., YYYY-MM-DD).
        time_off_types: The time off event types to be retrieved. List elements must be one of:
            "ABSENCE", "PUBLIC_HOLIDAY", or "NON_WORKING_DAY".

    Returns:
        The list of the user's time off events.
    """
    # accept list of enums in format that agent passes in, filter and use
    time_off_enum_list: List[TimeOffTypes] = string_to_list_of_enums(time_off_types, TimeOffTypes)
    assert len(time_off_enum_list) > 0
    filtered_time_off_list = [enum.name for enum in time_off_enum_list]

    client = get_sap_successfactors_client()

    response = client.get_time_management_request(
        endpoint="events",
        params={
            "assignmentId": user_id,
            "types": filtered_time_off_list,
            "startDate": start_date,
            "endDate": end_date,
        },
    )

    time_off_events = [
        UpcomingTimeOff(
            title=entry.get("title"),
            start_date=entry.get("startDate"),
            end_date=entry.get("endDate"),
            start_time=entry.get("startTime", None),
            end_time=entry.get("endTime", None),
            duration=entry.get("duration"),
            time_unit=entry.get("timeUnit"),
            cross_midnight=entry.get("crossMidnight"),
            type=entry.get("type"),
            status_formatted=entry.get("statusFormatted", None),
            absence_duration_category=entry.get("absenceDurationCategory", None),
        )
        for entry in response["value"]
    ]
    return UpcomingTimeOffResponse(time_off_events=time_off_events)
