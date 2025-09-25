from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.jira_client import get_jira_client
from agent_ready_tools.utils.tool_credentials import JIRA_CONNECTIONS


@dataclass
class Issue:
    """Represents an issue in Jira."""

    summary: str
    issue_number: str
    description: str
    author_name: str
    created_date: str
    file_name: Optional[str]
    progress_percent: int
    status: Optional[str]
    labels: List[Optional[str]]
    due_date: Optional[str]
    priority: Optional[str]


@dataclass
class IssuesResponse:
    """Represents the response for retrieving issues in Jira."""

    issues: List[Issue]
    next_page_token: Optional[str] = None


@tool(expected_credentials=JIRA_CONNECTIONS)
def get_issues(
    project_name: str,
    issue_number: Optional[str] = None,
    next_page_token: Optional[str] = None,
    limit: Optional[int] = 50,
) -> IssuesResponse:
    """
    Gets a list of issues from Jira.

    Args:
        project_name: The name of the project in Jira returned by the `get_projects` tool.
        issue_number: The number of the issue from a project in jira.
        next_page_token: A token used to skip a specific number of items for pagination purposes.
            Use this to retrieve subsequent pages of results when handling large datasets.
        limit: The maximum number of issues to retrieve in a single API call.The default value is
            50. Use this to control the size of the result set.

    Returns:
        List of issues from a project in jira.
    """
    client = get_jira_client()

    params: Dict[str, Any] = {}

    params = {
        "maxResults": limit,
        "nextPageToken": next_page_token,
        "expand": "versionedRepresentations",
        "fields": "summary,description,attachment,progress,labels,duedate,status,assignee,created,priority",
    }
    if issue_number:
        params["jql"] = f"project='{project_name}' and key='{issue_number}'"
    else:
        params["jql"] = f"project='{project_name}'"

    params = {key: value for key, value in params.items() if value}

    response = client.get_request("search/jql", params=params)

    issues: List[Issue] = []

    for item in response.get("issues", []):
        versioned_representations = item.get("versionedRepresentations", {})

        summary = versioned_representations.get("summary", {}).get("1", "")

        description = ""
        desc_obj = versioned_representations.get("description", {}).get("1")
        if isinstance(desc_obj, dict):
            outer_content = desc_obj.get("content", [])
            if outer_content and isinstance(outer_content, list):
                inner_content = (
                    outer_content[0].get("content", [])
                    if isinstance(outer_content[0], dict)
                    else []
                )
                if inner_content and isinstance(inner_content, list):
                    description = (
                        inner_content[0].get("text", "")
                        if isinstance(inner_content[0], dict)
                        else ""
                    )

        attachment_list = versioned_representations.get("attachment", {}).get("1")
        attachment = (
            attachment_list[0] if isinstance(attachment_list, list) and attachment_list else {}
        )
        file_name = attachment.get("filename", "") if isinstance(attachment, dict) else ""

        assignee = versioned_representations.get("assignee", {}).get("1")
        author_name = assignee.get("displayName", "") if isinstance(assignee, dict) else ""

        created_date = versioned_representations.get("created", {}).get("1", "")

        progress_percent = (
            versioned_representations.get("progress", {}).get("1", {}).get("progress", 0)
        )

        status = versioned_representations.get("status", {}).get("1", {}).get("name", "")

        labels = versioned_representations.get("labels", {}).get("1", [])

        due_date = versioned_representations.get("duedate", {}).get("1", "")

        priority_obj = versioned_representations.get("priority", {}).get("1", {})
        priority = priority_obj.get("name", "") if isinstance(priority_obj, dict) else ""

        issues.append(
            Issue(
                summary=summary,
                issue_number=item.get("key", ""),
                description=description,
                author_name=author_name,
                created_date=created_date,
                file_name=file_name,
                progress_percent=progress_percent,
                status=status,
                labels=labels,
                due_date=due_date,
                priority=priority,
            )
        )

    return IssuesResponse(issues=issues, next_page_token=response.get("nextPageToken", ""))
