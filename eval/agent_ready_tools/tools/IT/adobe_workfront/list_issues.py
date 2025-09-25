from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.tools.IT.adobe_workfront.adobe_workfront_schemas import (
    AdobeWorkfrontIssueStatus,
    AdobeWorkfrontPriority,
)
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class AdobeIssue:
    """Represents a single issue in Adobe Workfront."""

    issue_id: str
    issue_name: str
    percent_complete: Optional[int]
    planned_completion_date: Optional[str]
    issue_status: Optional[str]


@dataclass
class ListIssuesResponse:
    """Represents the response for retrieving issues in Adobe Workfront."""

    issues: List[AdobeIssue]


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def list_issues(
    issue_name: Optional[str] = None,
    limit: Optional[int] = 50,
    skip: Optional[int] = 0,
    assigned_to: Optional[str] = None,
    creation_date: Optional[str] = None,
    is_complete: Optional[bool] = False,
    issue_id: Optional[str] = None,
    percent_complete: Optional[int] = 0,
    priority: Optional[AdobeWorkfrontPriority] = None,
    project_id: Optional[str] = None,
    reference_number: Optional[int] = 0,
    issue_status: Optional[AdobeWorkfrontIssueStatus] = None,
) -> ListIssuesResponse:
    """
    Gets a list of issues from Adobe Workfront.

    Args:
        issue_name: The name of the issue in Adobe Workfront.
        limit: The maximum number of issues to retrieve in a single API call. Defaults to 50. Use
            this to control the size of the result set.
        skip: The number of issues to skip for pagination purposes. Use this to retrieve subsequent
            pages of results when handling large datasets.
        assigned_to: The user to whom the issue is assigned in Adobe Workfront, returned by the `list_users` tool.
        creation_date: The creation date of issue in ISO 8601 format (e.g., YYYY-MM-DD).
        is_complete: The completion of the issue. If True, only active issues are retrieved. If False,
            only inactive programs are retrieved.
        issue_id: The unique identifier of the issue in Adobe Workfront.
        percent_complete: The completed percentage of the issue in Adobe Workfront.
        priority: The priority of the issue in Adobe Workfront.
        project_id: The unique identifier of the project in Adobe Workfront, returned by `list_projects` tool.
        reference_number: The reference number of the issue in Adobe Workfront.
        issue_status: The status of the issue in Adobe Workfront.

    Returns:
        Result of get operation performed on issues.
    """

    client = get_adobe_workfront_client()
    params: Dict[str, Any] = {
        "name": issue_name,
        "$$LIMIT": limit,
        "$$FIRST": skip,
        "assignedToID": assigned_to,
        "entryDate": creation_date,
        "ID": issue_id,
        "isComplete": is_complete,
        "percentComplete": percent_complete,
        "priority": AdobeWorkfrontPriority[priority.upper()].value if priority else None,
        "projectID": project_id,
        "referenceNumber": reference_number,
        "status": AdobeWorkfrontIssueStatus[issue_status.upper()].value if issue_status else None,
    }

    params = {key: value for key, value in params.items() if value}

    response = client.get_request(entity="optask/search", params=params)

    issues: List[AdobeIssue] = [
        AdobeIssue(
            issue_id=result.get("ID", ""),
            issue_name=result.get("name", ""),
            percent_complete=result.get("percentComplete", 0),
            planned_completion_date=result.get("plannedCompletionDate", ""),
            issue_status=result.get("status", ""),
        )
        for result in response.get("data", [])
    ]

    return ListIssuesResponse(
        issues=issues,
    )
