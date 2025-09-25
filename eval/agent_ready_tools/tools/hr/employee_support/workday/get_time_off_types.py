from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.tools.hr.employee_support.workday.workday_schemas import (
    _TIME_OFF_CATEGORY_ID,
)
from agent_ready_tools.utils.tool_credentials import WORKDAY_CONNECTIONS


@dataclass(frozen=True)
class TimeOffType:
    """A single time off type in Workday."""

    type_id: str
    name: str
    daily_default_quantity: int
    unit_of_time: Optional[str]


@dataclass(frozen=True)
class GetTimeOffTypesResponse:
    """Represents the response from getting a list of time off types for a user."""

    time_off_types: list[TimeOffType]


@tool(expected_credentials=WORKDAY_CONNECTIONS)
def get_time_off_types(user_id: str) -> GetTimeOffTypesResponse:
    """
    Gets a list of eligible time off types for the specified user.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API, returned by the get_user_workday_ids tool.

    Returns:
        A list of time off types for the user.
    """
    client = get_workday_client()

    url = f"api/absenceManagement/v1/{client.tenant_name}/workers/{user_id}/eligibleAbsenceTypes"
    params = {
        "limit": "100",
        "offset": "0",
        # Return absences of "Time Off" type only.
        "category": _TIME_OFF_CATEGORY_ID,
    }

    response = client.get_request(url=url, params=params)

    time_off_types: list[TimeOffType] = []

    time_off_types_response = response.get("data")

    if time_off_types_response is not None:
        for time_off_type in time_off_types_response:

            unit_of_time = time_off_type.get("unitOfTime")

            time_off_types.append(
                TimeOffType(
                    type_id=time_off_type.get("id"),
                    name=time_off_type.get("descriptor"),
                    unit_of_time=(
                        unit_of_time.get("descriptor") if unit_of_time is not None else None
                    ),
                    daily_default_quantity=time_off_type.get("dailyDefaultQuantity"),
                )
            )

    return GetTimeOffTypesResponse(time_off_types=time_off_types)
