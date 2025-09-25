from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class JobChangeReasonCategory:
    """Represents a job change reasons category in Workday."""

    descriptor: str
    href: str


@dataclass
class JobChangeReasonsCategoryResponse:
    """Represents an available job change reasons category."""

    categories: list[JobChangeReasonCategory]


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_job_change_reasons_categories() -> JobChangeReasonsCategoryResponse:
    """
    Gets all configured job change reasons categories in Workday.

    Returns:
        The available job reasons categories for Workday.
    """

    client = get_workday_client()
    url = f"api/staffing/v6/{client.tenant_name}/values/jobChangesGroup/reason"
    response = client.get_request(url=url)

    return JobChangeReasonsCategoryResponse(
        categories=[
            JobChangeReasonCategory(
                descriptor=data.get("descriptor", ""), href=data.get("href", "")
            )
            for data in response.get("data", {})
        ]
    )
