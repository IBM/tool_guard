from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.tools.IT.adobe_workfront.adobe_workfront_schemas import (
    AdobeWorkfrontPriority,
)
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class AdobeCreateIssueResponse:
    """Represents the result for issue creation in Adobe Workfront."""

    issue_id: str
    issue_name: str


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def adobe_create_an_issue(
    project_id: str,
    issue_name: str,
    issue_description: Optional[str] = None,
    issue_priority: Optional[AdobeWorkfrontPriority] = None,
) -> AdobeCreateIssueResponse:
    """
    Creates a issue in Adobe Workfront.

    Args:
        project_id: The id of the project from Adobe Workfront, returned by the `list_projects`
            tool.
        issue_name: The name of the issue to be created in Adobe Workfront.
        issue_description: A detailed description of the issue to be created in Adobe Workfront.
        issue_priority: The priority level of the issue in Adobe Workfront.

    Returns:
        The result of creating a issue.
    """

    client = get_adobe_workfront_client()

    payload: dict[str, Any] = {
        "projectID": project_id,
        "name": issue_name,
        "description": issue_description,
        "priority": (
            int(AdobeWorkfrontPriority[issue_priority.upper()].value) if issue_priority else None
        ),
    }
    payload = {key: value for key, value in payload.items() if value}

    response = client.post_request(entity="optask", payload=payload)
    data = response.get("data", {})
    return AdobeCreateIssueResponse(issue_id=data.get("ID", ""), issue_name=data.get("name", ""))
