from datetime import date
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.tools.IT.adobe_workfront.adobe_workfront_schemas import (
    AdobeWorkfrontIssueStatus,
    AdobeWorkfrontPriority,
)
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class UpdateIssueResponse:
    """Represents the result of updating issue details in Adobe Workfront."""

    issue_id: str
    issue_name: str
    status: str


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def adobe_update_an_issue(
    issue_id: str,
    issue_name: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[AdobeWorkfrontPriority] = None,
    planned_start_date: Optional[date] = None,
    planned_completion_date: Optional[date] = None,
) -> UpdateIssueResponse:
    """
    Updates the issue details in Adobe Workfront.

    Args:
        issue_id: The id of an issue, returned by `list_issues` tool.
        issue_name: The name of an issue.
        description: The description of an issue.
        status: The status of an issue.
        priority: The priority of an issue.
        planned_start_date: The planned start date of an issue in ISO 8601 format (e.g., YYYY-MM-
            DD).
        planned_completion_date: The planned completion date of an issue in ISO 8601 format (e.g.,
            YYYY-MM-DD).

    Returns:
        Result of performing update operation on an issue.
    """
    client = get_adobe_workfront_client()

    payload = {
        "name": issue_name,
        "description": description,
        "status": status,
        "priority": int(AdobeWorkfrontPriority[priority.upper()].value) if priority else None,
        "plannedStartDate": planned_start_date,
        "plannedCompletionDate": planned_completion_date,
    }

    payload = {key: value for key, value in payload.items() if value}

    entity = f"optask/{issue_id}"
    response = client.put_request(entity=entity, payload=payload)

    issue_data = response.get("data", {})

    return UpdateIssueResponse(
        issue_id=issue_data.get("ID", ""),
        issue_name=issue_data.get("name", ""),
        status=AdobeWorkfrontIssueStatus(issue_data.get("status")).name,
    )
