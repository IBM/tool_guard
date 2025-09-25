from datetime import datetime, timedelta
from typing import Any

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS

_ACTION_WID: str = "d9e4223e446c11de98360015c5e6daf6"


# TODO Uncomment once Union support is added to the SDK
# @dataclass
# class TimeOffDate:
#     """Represents a single day that the user would like to request off."""
#
#     date: str
#     start_time: str
#     end_time: str
#     daily_quantity: int
#
#


@dataclass
class RequestedDayOff:
    """Represents a single day that the user requested off."""

    date: str
    description: str


@dataclass
class WorkdayRequestTimeOffResponse:
    """Represents the result of a time off request operation in Workday."""

    request_id: str
    request_description: str
    request_status: str
    requested_days: list[RequestedDayOff]


def _request_time_off_payload(
    time_off_start_date: str,
    time_off_end_date: str,
    time_off_type_id: str,
    default_daily_quantity: str,
) -> dict:
    """
    Returns a payload object of type dict filled.

    Args:
        time_off_start_date: specified in ISO 8601 format (e.g., YYYY-MM-DD).
        time_off_end_date: specified in ISO 8601 format (e.g., YYYY-MM-DD).
        time_off_type_id: The ID of the time off type, as specified by the `get_time_off_types`
            tool.
        default_daily_quantity: The default daily quantity of the time off type, as specified by the `get_time_off_types`
            tool.

    Returns:
        dictionary
    """
    payload: dict[str, Any] = {
        "businessProcessParameters": {"action": {"id": _ACTION_WID}},
        "days": [],
    }

    start_date = datetime.strptime(time_off_start_date, "%Y-%m-%d")
    end_date = datetime.strptime(time_off_end_date, "%Y-%m-%d")
    delta = end_date - start_date
    for i in range(delta.days + 1):
        date = (start_date + timedelta(days=i)).date()

        if date.weekday() >= 5:  # Do not submit time off requests on the weekend
            pass

        payload["days"].append(
            {
                "date": str(date),
                "dailyQuantity": default_daily_quantity,
                # TODO This implementation assumes the user is taking a full day off. Revise as necessary
                "timeOffType": {"id": time_off_type_id},
            }
        )
    return payload


# TODO Add support for requesting *partial* days off
@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def request_time_off(
    user_id: str,
    time_off_start_date: str,
    time_off_end_date: str,
    time_off_type_id: str,
    default_daily_quantity: str,
) -> WorkdayRequestTimeOffResponse:
    """
    Creates a time off request for the user in Workday.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API.
        time_off_start_date: specified in ISO 8601 format (e.g., YYYY-MM-DD).
        time_off_end_date: specified in ISO 8601 format (e.g., YYYY-MM-DD).
        time_off_type_id: The ID of the time off type, as specified by the `get_time_off_types`
            tool.
        default_daily_quantity: The default daily quantity of the time off type, as specified by the `get_time_off_types`
            tool.

    Returns:
        The result from making the time off request for the user.
    """
    client = get_workday_client()

    response = client.request_time_off(
        user_id,
        payload=_request_time_off_payload(
            time_off_start_date=time_off_start_date,
            time_off_end_date=time_off_end_date,
            time_off_type_id=time_off_type_id,
            default_daily_quantity=default_daily_quantity,
        ),
    )

    requested_days: list[RequestedDayOff] = []
    for requested_day in response["days"]:
        requested_days.append(
            RequestedDayOff(date=requested_day["date"], description=requested_day["descriptor"])
        )
    requested_days.sort(key=lambda day: day.date)

    return WorkdayRequestTimeOffResponse(
        request_id=response["businessProcessParameters"]["overallBusinessProcess"]["id"],
        request_description=response["businessProcessParameters"]["overallBusinessProcess"][
            "descriptor"
        ],
        request_status=response["businessProcessParameters"]["overallStatus"],
        requested_days=requested_days,
    )
