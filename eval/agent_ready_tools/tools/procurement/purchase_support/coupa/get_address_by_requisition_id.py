from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaAddress,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_helper_functions import (
    coupa_build_address,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_address_by_requisition_id(
    requisition_id: int,
) -> ToolResponse[CoupaAddress]:
    """
    Retrieves the shipping address from a requisition if there is one.

    Args:
        requisition_id: The requisition ID that is being checked for an address.

    Returns:
        The resulting shipping address or None if the requisition doesn't have a shipping address.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request(resource_name=f"requisitions/{requisition_id}")
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    ship_to_address = response.get("ship-to-address")
    if not ship_to_address:
        return ToolResponse(success=False, message="Requisition has no shipping address.")

    return ToolResponse(
        success=True,
        message="Address retrieved successfully.",
        content=coupa_build_address(address=ship_to_address),
    )
