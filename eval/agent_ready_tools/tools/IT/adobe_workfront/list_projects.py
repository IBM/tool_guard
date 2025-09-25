from typing import Any, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.tools.IT.adobe_workfront.adobe_workfront_schemas import (
    AdobeWorkfrontPriority,
    AdobeWorkfrontProjectStatus,
)
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class Project:
    """Represents the response for retrieving a project in Adobe Workfront."""

    project_id: str
    project_name: str
    projected_completion_date: Optional[str]
    priority: Optional[str]
    status: Optional[str]


@dataclass
class ListProjectsResponse:
    """Represents the response for retrieving projects in Adobe Workfront."""

    projects: List[Project]


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def list_projects(
    project_name: Optional[str] = None,
    priority: Optional[AdobeWorkfrontPriority] = None,
    status: Optional[AdobeWorkfrontProjectStatus] = None,
    limit: Optional[int] = 100,
    skip: Optional[int] = 0,
) -> ListProjectsResponse:
    """
    Gets a list of projects from Adobe Workfront.

    Args:
        project_name: The name of the project in Adobe Workfront.
        priority: The priority of the project in Adobe Workfront.
        status: The status of the project in Adobe Workfront.
        limit: The maximum number of projects to return. Default is 100.
        skip: The number of projects to skip (for pagination). Default is 0.

    Returns:
        List of projects in Adobe Workfront.
    """

    client = get_adobe_workfront_client()

    params: dict[str, Any] = {
        "name": project_name,
        "priority": AdobeWorkfrontPriority[priority.upper()].value if priority else None,
        "status": AdobeWorkfrontProjectStatus[status.upper()].value if status else None,
        "$$LIMIT": limit,
        "$$FIRST": skip,
    }

    params = {key: value for key, value in params.items() if value}

    response = client.get_request(entity="proj/search", params=params)

    projects: List[Project] = [
        Project(
            project_id=result.get("ID", ""),
            project_name=result.get("name", ""),
            projected_completion_date=result.get("projectedCompletionDate", ""),
            priority=(
                AdobeWorkfrontPriority(str(result.get("priority"))).name
                if result.get("priority", "")
                else ""
            ),
            status=AdobeWorkfrontProjectStatus(
                result.get("status", AdobeWorkfrontProjectStatus.PLANNING)
            ).name,
        )
        for result in response.get("data", [])
    ]

    return ListProjectsResponse(
        projects=projects,
    )
