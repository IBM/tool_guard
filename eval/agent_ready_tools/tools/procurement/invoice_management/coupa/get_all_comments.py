from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.invoice_management.coupa.common_classes_invoice_management import (
    CoupaComments,
    CoupaCommentsList,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_all_comments(commentable_id: int) -> ToolResponse[CoupaCommentsList]:
    """
    delete invoice all comments.

    Args:
        commentable_id: a unique commentable identifier

    Returns:
        true if succeeded, false otherwise
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    resource_name = "comments"
    params = {"commentable-id": commentable_id}
    response = client.get_request_list(resource_name=resource_name, params=params)
    if len(response) == 1 and "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    if not isinstance(response, list) or len(response) == 0:
        return ToolResponse(success=True, message="There are no comments on this invoice.")

    coupa_comments: List[CoupaComments] = []
    for comment in response:
        assert isinstance(comment, dict)
        coupa_comment = CoupaComments(
            id=comment["id"],
            created_at=comment.get("created-at"),
            updated_at=comment.get("updated-at"),
            commentable_id=comment.get("commentable-id"),
            commentable_type=comment.get("commentable-type"),
            reason_code=comment.get("reason-code"),
            to_supplier=comment.get("to-supplier"),
            comment_type=comment.get("comment-type"),
            comments=comment.get("comments"),
            comments_with_mentions_uniq_id=comment.get("comments-with-mentions-uniq-id"),
            allow_edit=comment.get("allow-edit"),
            allow_delete=comment.get("allow-delete"),
            is_read=comment.get("is-read"),
            modified=comment.get("modified"),
        )
        coupa_comments.append(coupa_comment)

    return ToolResponse(
        success=True,
        message="Following is the list of comments.",
        content=CoupaCommentsList(coupa_comments),
    )
