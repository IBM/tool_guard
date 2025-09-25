from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.tools.hr.employee_support.workday.workday_schemas import (
    _TIME_OFF_CATEGORY_ID,
)
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class TimeOffEntry:
    """A single time off entry in Workday."""

    status: str
    time_off_type: str
    quantity: str
    unit: str
    date: str


@dataclass
class GetTimeOffResponse:
    """Represents the response from getting a user's time off entries in Workday."""

    time_off_entries: List[TimeOffEntry]


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_time_off(
    user_id: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    status_type_id: Optional[str] = None,
    time_off_type_id: Optional[str] = None,
) -> GetTimeOffResponse:
    """
    Gets a user's time off entries in Workday.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API.
        from_date: The start of a date range filter in ISO 8601 format (e.g., YYYY-MM-DD).
        to_date: The end of a date range filter in ISO 8601 format (e.g., YYYY-MM-DD).
        status_type_id: The type_id of the status type, as specified by the
            `get_time_off_status_types` tool.
        time_off_type_id: The type_id of the time off type, as specified by the `get_time_off_types`
            tool.

    Returns:
        The user's time off entries.
    """
    client = get_workday_client()

    params = {
        "fromDate": from_date,
        "toDate": to_date,
        "status": status_type_id,
        "timeOffType": time_off_type_id,
        "category": _TIME_OFF_CATEGORY_ID,
    }
    params = {key: value for key, value in params.items() if value is not None}

    url = f"api/absenceManagement/v1/{client.tenant_name}/workers/{user_id}/timeOffDetails"
    response = client.get_request(url=url, params=params)

    time_off_entries: list[TimeOffEntry] = []
    for time_off_entry in response.get("data", []):
        time_off_entries.append(
            TimeOffEntry(
                status=time_off_entry["status"]["descriptor"],
                time_off_type=time_off_entry["timeOffType"]["descriptor"],
                quantity=time_off_entry["quantity"],
                unit=time_off_entry["unit"]["descriptor"],
                date=time_off_entry["date"],
            )
        )
    return GetTimeOffResponse(time_off_entries=time_off_entries)
