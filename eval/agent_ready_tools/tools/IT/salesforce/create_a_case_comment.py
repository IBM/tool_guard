from typing import Any

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@dataclass
class CreateCommentResponse:
    """Represents the result of adding a comment for a case in Salesforce."""

    comment_id: str


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def create_a_case_comment(case_id: str, comment: str) -> CreateCommentResponse:
    """
    Creates a comment for a case in Salesforce.

    Args:
        case_id: The id of the case in Salesforce returned by the `list_cases` tool.
        comment: The comment to be added for a case in Salesforce.

    Returns:
        The result of performing the creation of comment for a case.
    """
    client = get_salesforce_client()

    payload: dict[str, Any] = {
        "ParentId": case_id,
        "CommentBody": comment,
    }

    response = client.salesforce_object.CaseComment.create(data=payload)  # type: ignore[operator]

    return CreateCommentResponse(comment_id=response.get("id", ""))
