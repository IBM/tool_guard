from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.box_client import get_box_client
from agent_ready_tools.utils.tool_credentials import BOX_CONNECTIONS


@dataclass
class UpdateACommentResponse:
    """Represents the response of updating a comment in a Box file."""

    message: str


@tool(expected_credentials=BOX_CONNECTIONS)
def update_a_comment(original_comment_id: str, new_comment: str) -> UpdateACommentResponse:
    """
    Updates a comment in a Box file.

    Args:
        original_comment_id: The comment_id of the original_comment returned by the `get_comments`
            tool.
        new_comment: The new comment to be updated.

    Returns:
        Confirmation of the comment update.
    """

    client = get_box_client()
    payload = {"message": new_comment}

    response = client.put_request(
        entity=f"comments/{original_comment_id}",
        data=payload,
    )

    message = response.get("message", "")

    return UpdateACommentResponse(message=message)
