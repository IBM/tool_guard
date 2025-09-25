from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class TimeOffStatusType:
    """A single time off status type in Workday."""

    status_type: str
    type_id: str


@dataclass
class GetTimeOffStatusTypesResponse:
    """The time off status types configured for a Workday deployment."""

    status_types: list[TimeOffStatusType]


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_time_off_status_types() -> GetTimeOffStatusTypesResponse:
    """
    Gets a list of time off status types configured for this Workday deployment.

    Returns:
        The list of status types.
    """
    client = get_workday_client()

    url = f"api/absenceManagement/v1/{client.tenant_name}/values/timeOff/status"
    response = client.get_request(url=url)

    status_types: list[TimeOffStatusType] = []
    for status_type in response.get("data", []):
        status_types.append(
            TimeOffStatusType(status_type=status_type["descriptor"], type_id=status_type["id"])
        )
    return GetTimeOffStatusTypesResponse(status_types=status_types)
