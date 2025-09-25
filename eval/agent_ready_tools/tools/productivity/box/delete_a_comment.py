from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.box_client import get_box_client
from agent_ready_tools.utils.tool_credentials import BOX_CONNECTIONS


@dataclass
class DeleteACommentResponse:
    """Represents the response of deleting a comment in Box."""

    http_code: int


@tool(expected_credentials=BOX_CONNECTIONS)
def delete_a_comment(comment_id: str) -> DeleteACommentResponse:
    """
    Deletes a comment in Box file.

    Args:
        comment_id: The comment_id of the comment returned by the `get_comments` tool.

    Returns:
        Confirmation of the comment deletion.
    """

    client = get_box_client()

    response = client.delete_request(entity=f"comments/{comment_id}")
    return DeleteACommentResponse(http_code=response)
