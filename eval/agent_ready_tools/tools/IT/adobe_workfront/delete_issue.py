from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class AdobeDeleteIssueResponse:
    """Represents the result of delete operation performed on an issue in Adobe Workfront."""

    http_code: int


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def delete_issue(issue_id: str) -> AdobeDeleteIssueResponse:
    """
    Deletes an issue in Adobe Workfront.

    Args:
        issue_id: The id of the issue, returned by the `list_issues` tool.

    Returns:
        The status of the delete operation.
    """

    client = get_adobe_workfront_client()

    response = client.delete_request(entity=f"optask/{issue_id}")
    return AdobeDeleteIssueResponse(http_code=response)
