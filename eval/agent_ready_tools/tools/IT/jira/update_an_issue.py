from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.jira_client import get_jira_client
from agent_ready_tools.utils.tool_credentials import JIRA_CONNECTIONS


@dataclass
class UpdateAnIssueResponse:
    """Represents the result of updating issue details in Jira."""

    http_code: int


@tool(expected_credentials=JIRA_CONNECTIONS)
def update_an_issue(
    issue_number: str,
    summary: Optional[str] = None,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    account_id: Optional[str] = None,
    label: Optional[str] = None,
    priority: Optional[str] = None,
) -> UpdateAnIssueResponse:
    """
    Updates issue details in Jira.

    Args:
        issue_number: The issue_number, returned by the `get_issues` tool.
        summary: The new summary of the issue in Jira.
        description: The new description of the issue in Jira.
        due_date: The due date for the issue in Jira in ISO 8601 format (e.g., YYYY-MM-DD).
        account_id: The account_id of the assignee, returned by the `get_users` tool.
        label: A label to categorize the issue in Jira.
        priority: The priority of the issue, returned by the `get_issue_priorities` tool.

    Returns:
        Confirmation of the details update.
    """
    client = get_jira_client()

    payload: dict[str, Any] = {
        "fields": {
            "summary": summary,
            "description": (
                {
                    "content": [
                        {
                            "content": [{"text": description, "type": "text"}],
                            "type": "paragraph",
                        }
                    ],
                    "type": "doc",
                    "version": 1,
                }
                if description
                else None
            ),
            "priority": {"name": priority} if priority else None,
            "duedate": due_date,
            "assignee": {"accountId": account_id} if account_id else None,
        },
        "update": {"labels": [{"add": label}]} if label else None,
    }
    # Remove None values from the payload
    payload = {
        key: value for key, value in payload.items() if value
    }  # It will perform a first level object check
    payload["fields"] = {
        key: value for key, value in payload.get("fields", {}).items() if value is not None
    }  # It will perform a second level object check
    entity = f"issue/{issue_number}"
    response = client.put_request(entity=entity, payload=payload)
    return UpdateAnIssueResponse(http_code=response.get("status_code", ""))
