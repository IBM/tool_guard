from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import AccessLevel
from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class JobChangeResponse:
    """Represents the response to a job change request."""

    error: Optional[str]
    status: Optional[str]


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def initiate_location_change(
    worker_id: str, location_id: str, reason_id: str, effective_date: str
) -> JobChangeResponse:
    """
    Initiates a location change request in Workday.

    Args:
        worker_id: The user's worker_id uniquely identifying them within the Workday API.
        location_id: The location id returned by the `get_job_change_locations` tool.
        reason_id: The reason id returned by the `get_job_change_reasons` tool.
        effective_date: The effective date user change take place in ISO 8601 format.

    Returns:
        The result from performing a location change to the user's.
    """

    client = get_workday_client(access_level=AccessLevel.MANAGER)
    body = {"date": effective_date, "reason": {"id": reason_id}, "location": {"id": location_id}}

    response = client.initiate_job_change(worker_id, body)

    error = response.get("error", None)
    if error is not None:
        return JobChangeResponse(error=error, status=None)
    else:
        job_change_id = response["id"]
        submit_response = client.submit_job_change(job_change_id)
        error = submit_response.get("error", None)
        if error is not None:
            return JobChangeResponse(error=error, status=None)
        else:
            return JobChangeResponse(
                error=None, status=submit_response.get("status", {}).get("descriptor", "")
            )
