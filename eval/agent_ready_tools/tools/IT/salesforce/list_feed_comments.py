from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import FeedComment
from agent_ready_tools.utils.sql_utils import format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_feed_comments(search: Optional[str] = None) -> list[FeedComment]:
    """
    Returns a list of feed comments within Salesforce.

    Args:
        search: The SQL where clause from LLM (to clean up).

    Returns:
        A list of feed comments in Salesforce.
    """
    client = get_salesforce_client()
    cleaned_clause = format_where_input_string(search or "")

    rs = client.salesforce_object.query_all_iter(
        format_soql(
            f"SELECT Id, CommentBody, FeedItemId, ParentId, IsRichText, Status, CreatedById, CreatedDate FROM FeedComment {cleaned_clause}"
        )
    )

    results: list[FeedComment] = []

    for obj in rs:
        results.append(
            FeedComment(
                feed_comment_id=obj.get("Id", ""),
                comment=obj.get("CommentBody", ""),
                feed_item_id=obj.get("FeedItemId", ""),
                parent_id=obj.get("ParentId", ""),
                is_rich_text=obj.get("IsRichText", ""),
                status=obj.get("Status", ""),
                created_by_id=obj.get("CreatedById", ""),
                created_date=obj.get("CreatedDate", ""),
            )
        )

    return results
