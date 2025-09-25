from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.jira_client import get_jira_client
from agent_ready_tools.utils.tool_credentials import JIRA_CONNECTIONS


@dataclass
class CreateIssueResponse:
    """Represents the result for issue creation in Jira."""

    issue_number: str


@tool(expected_credentials=JIRA_CONNECTIONS)
def create_an_issue(
    project_id: str,
    issuetype_id: str,
    summary: str,
    description: Optional[str] = None,
    label: Optional[str] = None,
    priority: Optional[str] = None,
) -> CreateIssueResponse:
    """
    Creates an issue in Jira.

    Args:
        project_id: The ID of the project in Jira returned by the `get_projects` tool.
        issuetype_id: The ID of the issue type in Jira returned by the `get_project_issue_types`
            tool using project_id of the current tool.
        summary: The summary of the issue in Jira.
        description: A detailed explanation of the issue in Jira.
        label: A label to categorize the issue in Jira.
        priority: The priority level of the issue in Jira returned by the `get_issue_priorities`
            tool.

    Returns:
        The result of creating an issue.
    """

    client = get_jira_client()

    payload: dict[str, Any] = {
        "fields": {
            "project": {"id": project_id},
            "issuetype": {"id": issuetype_id},
            "summary": summary,
            "description": (
                {
                    "content": [
                        {"content": [{"text": description, "type": "text"}], "type": "paragraph"}
                    ],
                    "type": "doc",
                    "version": 1,
                }
                if description
                else None
            ),
            "labels": [label] if label else None,
            "priority": {"name": priority} if priority else None,
        }
    }
    payload["fields"] = {key: value for key, value in payload.get("fields", {}).items() if value}
    response = client.post_request(entity="issue", payload=payload)
    return CreateIssueResponse(issue_number=response.get("key", ""))
