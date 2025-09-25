from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class JobChangeReason:
    """Represents a job change reason in Workday."""

    descriptor: str
    id: str


@dataclass
class JobChangeReasonsResponse:
    """Represents the available job change reasons."""

    reasons: list[JobChangeReason]


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_job_change_reasons_by_category(group_id: str, category_id: str) -> JobChangeReasonsResponse:
    """
    Gets all configured job change reasons from the selected category in Workday.

    Args:
        group_id: Group ID to filter Job Change Reasons
        category_id: Job Change Reason category ID

    Returns:
        The available job change reasons in the requested category.
    """

    client = get_workday_client()
    url = f"api/staffing/v6/{client.tenant_name}/values/jobChangesGroup/reason/{group_id}/{category_id}"
    response = client.get_request(url=url)

    return JobChangeReasonsResponse(
        reasons=[
            JobChangeReason(descriptor=data.get("descriptor", ""), id=data.get("id", ""))
            for data in response.get("data", {})
        ]
    )
