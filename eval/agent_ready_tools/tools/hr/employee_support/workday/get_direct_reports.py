from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class WorkdayDirectReport:
    """Represents a direct report in Workday."""

    user_id: str
    name: str
    business_title: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


@dataclass
class WorkdayDirectReportsResponse:
    """Represents the response from getting a user's direct reports in Workday."""

    direct_reports: list[WorkdayDirectReport]
    total: int


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_direct_reports(user_id: str) -> WorkdayDirectReportsResponse:
    """
    Gets a user's direct reports in Workday.

    Args:
        user_id: The user id uniquely identifying and return fron the get_user_workday_ids tool.

    Returns:
        The user's direct reports.
    """
    client = get_workday_client()

    url = f"api/v1/{client.tenant_name}/workers/{user_id}/directReports"

    response = client.get_request(url=url)

    direct_reports: list[WorkdayDirectReport] = []
    for report in response["data"]:
        direct_reports.append(
            WorkdayDirectReport(
                user_id=report["id"],
                name=report["descriptor"],
                business_title=report.get("businessTitle", None),
                email=report.get("primaryWorkEmail", None),
                phone=report.get("primaryWorkPhone", None),
            )
        )
    return WorkdayDirectReportsResponse(direct_reports=direct_reports, total=response["total"])
