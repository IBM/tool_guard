from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class UpdateProjectResponse:
    """Represents the result for project update in Adobe Workfront."""

    project_id: str
    name: str
    status: str


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def update_project(
    project_id: str,
    project_name: str,
    priority: Optional[str] = None,
    planned_start_date: Optional[str] = None,
    status: Optional[str] = None,
    owner_id: Optional[str] = None,
    program_id: Optional[str] = None,
    portfolio_id: Optional[str] = None,
) -> UpdateProjectResponse:
    """
    Updates a project in Adobe Workfront using the project ID.

    Args:
        project_id: The ID of the project to update, returned from the `list_projects` tool.
        project_name: The name of the project to update, returned from the `list_projects` tool.
        priority: The priority of the project (e.g., "High", "Medium", "Low").
        planned_start_date: The planned start date in ISO format (YYYY-MM-DD).
        status: The status of the project.
        owner_id: The ID of the owner to assign to the project.
        program_id: The ID of the program to assign to the project, returned from the
            `list_programs` tool.
        portfolio_id: The ID of the portfolio to assign to the project, returned from the
            `list_portfolios` tool.

    Returns:
        The result of updating a project.
    """

    client = get_adobe_workfront_client()

    payload = {
        "name": project_name,
        "priority": priority,
        "planned_start_date": planned_start_date,
        "status": status,
        "owner_id": owner_id,
        "program_id": program_id,
        "portfolio_id": portfolio_id,
    }
    payload = {key: value for key, value in payload.items() if value}

    update_response = client.put_request(entity=f"proj/{project_id}", payload=payload)
    data = update_response.get("data", {})

    return UpdateProjectResponse(
        project_id=data.get("ID", project_id),
        name=data.get("name", ""),
        status=data.get("status", ""),
    )
