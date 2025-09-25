from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.jira_client import get_jira_client
from agent_ready_tools.utils.tool_credentials import JIRA_CONNECTIONS


@dataclass
class DeleteIssueResponse:
    """Represents the result of delete an issue operation in Jira."""

    http_code: int


@tool(expected_credentials=JIRA_CONNECTIONS)
def delete_an_issue(
    issue_number: str, delete_sub_tasks: Optional[str] = "true"
) -> DeleteIssueResponse:
    """
    Deletes an issue in Jira.

    Args:
        issue_number: The issue_number uniquely identifying the issue, returned by `get_issues`
            tool.
        delete_sub_tasks: Indicates whether to delete the subtasks of an issue. Valid values are
            'true' or 'false'.

    Returns:
        The result of performing the delete operation on an issue.
    """

    client = get_jira_client()

    response = client.delete_request(
        entity=f"issue/{issue_number}?deleteSubtasks={delete_sub_tasks}"
    )

    return DeleteIssueResponse(http_code=response)
