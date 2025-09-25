from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def update_feed_comment(
    feed_comment_id: str,
    comment: str,
    status: Optional[str] = None,
    is_rich_text: Optional[bool] = True,
) -> int:
    """
    Updates a feed comment for in Salesforce.

    Args:
        feed_comment_id: The id of the feed comment in Salesforce returned by the
            `list_feed_comments` tool.
        comment: The feed comment to be updated in Salesforce.
        status: The status of the feed comment in Salesforce, possible values are Published,
            PendingReview and Isolated.
        is_rich_text: Indicates whether the feed comment in Salesforce contains rich text.

    Returns:
        The result of performing the update of feed comment in Salesforce.
    """
    client = get_salesforce_client()

    payload: dict[str, Any] = {"CommentBody": comment, "Status": status, "IsRichText": is_rich_text}

    response = client.salesforce_object.FeedComment.update(feed_comment_id, data=payload)  # type: ignore[operator]

    return response
