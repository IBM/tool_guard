from datetime import datetime, timezone
import re
from typing import Match, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import CaseComment
from agent_ready_tools.utils.sql_utils import format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


def format_date_only(match: Match[str]) -> str:
    """
    Converts a date string from 'YYYY-MM-DD' format to 'YYYY-MM-DDTHH:MM:SSZ' format.

    Args:
        match: A regex match object containing the date string.

    Returns:
        A string representing the date in 'YYYY-MM-DDTHH:MM:SSZ' format.
    """
    date_str = match.group(0)
    dt = datetime.strptime(date_str.strip(), "%Y-%m-%d")
    dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_case_comments(search: Optional[str] = None) -> list[CaseComment]:
    """
    Returns the list of all comments for a case in Salesforce.

    Args:
        search: The SQL where clause from LLM (to clean up).

    Returns:
        A list of CaseComment objects representing the comments in Salesforce.
    """
    client = get_salesforce_client()

    cleaned_clause = format_where_input_string(search or "")

    # Replace any 'YYYY-MM-DD' date strings in the cleaned clause
    cleaned_clause = re.sub(r"\d{4}-\d{2}-\d{2}", format_date_only, cleaned_clause)

    response = client.salesforce_object.query_all_iter(
        format_soql(
            f"SELECT Id, CommentBody, ParentId, CreatedDate, IsPublished FROM CaseComment {cleaned_clause}"
        )
    )

    results: list[CaseComment] = []
    for comment in response:
        results.append(
            CaseComment(
                comment_id=comment.get("Id"),
                case_id=comment.get("ParentId"),
                comment=comment.get("CommentBody"),
                comment_created_date=comment.get("CreatedDate"),
                published=comment.get("IsPublished"),
            )
        )
    return results
