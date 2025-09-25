from datetime import date

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class JobPosition:
    """Represents a job positions."""

    id: str
    descriptor: str


@dataclass
class JobPositionResponse:
    """Represents a response from Workday."""

    job_positions: list[JobPosition]
    total: int


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_job_positions(user_id: str, effective_date: date) -> JobPositionResponse:
    """
    Gets a job change reason in Workday.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API.
        effective_date: Date to take place of the change.

    Returns:
        The job positions available for the user.
    """
    client = get_workday_client()

    url = f"api/staffing/v5/{client.tenant_name}/values/jobChangesGroup/jobs"
    params = {"worker": user_id, "effectiveDate": str(effective_date)}

    response = client.get_request(url=url, params=params)

    job_positions: list[JobPosition] = []
    for report in response["data"]:
        job_positions.append(
            JobPosition(id=report.get("id", ""), descriptor=report.get("descriptor", ""))
        )
    return JobPositionResponse(job_positions=job_positions, total=response["total"])
