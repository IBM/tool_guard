from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaComment,
    CoupaCommentList,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_helper_functions import (
    coupa_build_comment_from_response,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_purchase_order_comments(purchase_order_id: int) -> ToolResponse[CoupaCommentList]:
    """
    Retrieves the comments of a purchase order.

    Args:
        purchase_order_id: The id of the purchase order.

    Returns:
        The retrieved list of comments of the purchase order.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")
    response = client.get_request_list(
        resource_name=f"purchase_orders/{purchase_order_id}/comments"
    )
    if len(response) == 0:
        return ToolResponse(success=False, message="No comments found.")

    if "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    comment_list: List[CoupaComment] = []
    for comment in response:
        comment_list.append(coupa_build_comment_from_response(comment))

    return ToolResponse(
        success=True,
        message="Comments retrieved successfully.",
        content=CoupaCommentList(comment_list=comment_list),
    )
