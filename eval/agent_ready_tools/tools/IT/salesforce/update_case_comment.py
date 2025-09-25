from typing import Any

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@dataclass
class UpdateCommentResponse:
    """Represents the result of updating a comment for a case in Salesforce."""

    http_code: int


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def update_case_comment(comment_id: str, comment: str) -> UpdateCommentResponse:
    """
    Updates a comment for a case in Salesforce.

    Args:
        comment_id: The id of the comment in Salesforce returned by the `list_case_comments` tool.
        comment: The comment to be updated for a case in Salesforce.

    Returns:
        The status of the update operation performed on the comment.
    """
    client = get_salesforce_client()

    payload: dict[str, Any] = {
        "CommentBody": comment,
    }

    response = client.salesforce_object.CaseComment.update(comment_id, data=payload)  # type: ignore[operator]

    return UpdateCommentResponse(http_code=response)
