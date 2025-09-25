from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.tools.IT.adobe_workfront.adobe_workfront_schemas import (
    AdobeWorkfrontPriority,
    AdobeWorkfrontProjectStatus,
)
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class CreateProjectResponse:
    """Represents the result of creating a project in Adobe Workfront."""

    project_name: str
    project_id: str
    status: Optional[str]


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def create_project(
    portfolio_id: str,
    name: str,
    planned_start_date: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[AdobeWorkfrontPriority] = None,
    fixed_revenue: Optional[float] = 0.0,
) -> CreateProjectResponse:
    """
    Creates a new project in Adobe Workfront.

    Args:
        portfolio_id: The portfolio_id uniquely identifying them within Adobe Workfront, is returned
            by the `list_portfolios` tool.
        name: The name of the new project in Adobe Workfront.
        planned_start_date: The planned start date of the project in Adobe Workfront.
        description: A brief description of the project in Adobe Workfront.
        priority: The priority level of the project in Adobe Workfront.
        fixed_revenue: The fixed revenue associated with the project in Adobe Workfront.

    Returns:
        The result of the create operation performed for a project in Adobe Workfront.
    """
    client = get_adobe_workfront_client()

    payload: Dict[str, Any] = {
        "portfolioID": portfolio_id,
        "name": name,
        "plannedStartDate": planned_start_date,
        "description": description,
        "priority": AdobeWorkfrontPriority[priority.upper()].value if priority else None,
        "fixedRevenue": fixed_revenue,
    }

    payload = {key: value for key, value in payload.items() if value is not None}

    response = client.post_request(entity="proj", payload=payload)

    project_data = response.get("data", {})
    return CreateProjectResponse(
        project_name=project_data.get("name", ""),
        project_id=project_data.get("ID", ""),
        status=AdobeWorkfrontProjectStatus(project_data.get("status", "PLN")).name,
    )
