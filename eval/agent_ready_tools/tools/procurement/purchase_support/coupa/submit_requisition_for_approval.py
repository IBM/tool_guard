from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaRequisition,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_helper_functions import (
    coupa_build_requisition_from_response,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_submit_requisition_for_approval(
    requisition_id: int,
) -> ToolResponse[CoupaRequisition]:
    """
    Submits an existing requisition for approval in Coupa.

    Args:
        requisition_id: The ID of the requisition in Coupa.

    Returns:
        boolean whether the requisition was submitted for approval successfully or not.
    """
    try:
        client = get_coupa_client(scope=["core.requisition.read", "core.requisition.write"])
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")
    requisition = client.get_request(resource_name=f"requisitions/{requisition_id}")
    if "errors" in requisition:
        return ToolResponse(success=False, message=coupa_format_error_string(requisition))

    # 3 main conditions to check for before submitting for approval to avoid pending_buyer_action stuff
    if requisition.get("status", "") != "draft":
        return ToolResponse(success=False, message="Status should be in 'draft'.")

    if requisition.get("line-count", 0) <= 0:
        return ToolResponse(success=False, message="Requisition Lines must not be empty.")

    if not requisition.get("ship-to-address", {}):
        return ToolResponse(success=False, message="Requisition must contain a ship-to-address.")

    response = client.put_request(
        resource_name=f"requisitions/{requisition_id}/update_and_submit_for_approval"
    )
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="Requisition submitted successfully",
        content=coupa_build_requisition_from_response(response),
    )
