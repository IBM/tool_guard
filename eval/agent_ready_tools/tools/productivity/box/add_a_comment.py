from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.box_client import get_box_client
from agent_ready_tools.utils.tool_credentials import BOX_CONNECTIONS


@dataclass
class AddACommentResult:
    """Represents the result of add a comment in Box."""

    comment_id: str
    comment: str


@tool(expected_credentials=BOX_CONNECTIONS)
def add_a_comment(
    file_id: str,
    comment: str,
) -> AddACommentResult:
    """
    Adds a comment for a Box file.

    Args:
        file_id: The id for the file returned by `get_file_details_by_name` tool.
        comment: The comment message for the file.

    Returns:
        The result from performing the add a comment.
    """
    client = get_box_client()

    payload = {"item": {"id": file_id, "type": "file"}, "message": comment}
    response = client.post_request(entity="comments", data=payload)

    return AddACommentResult(comment_id=response.get("id", ""), comment=response.get("message", ""))
