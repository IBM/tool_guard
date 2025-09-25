from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaComment,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_helper_functions import (
    coupa_build_comment_from_response,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_add_comment_to_requisition(
    requisition_id: int,
    comment_text: str,
) -> ToolResponse[CoupaComment]:
    """
    Adds a comment to an existing requisition in Coupa.

    Args:
        requisition_id: ID of the requisition for the comment to be added to.
        comment_text: The comment text to add to the requisition comments.

    Returns:
        The created comment.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    payload = {"comments": comment_text}

    response = client.post_request(
        resource_name=f"requisitions/{requisition_id}/comments", payload=payload
    )
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="Comment was added successfully.",
        content=coupa_build_comment_from_response(response),
    )
