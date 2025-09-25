from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaPurchaseOrder,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_helper_functions import (
    coupa_build_purchase_order_from_response,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_purchase_order_by_id(purchase_order_id: int) -> ToolResponse[CoupaPurchaseOrder]:
    """
    Gets a purchase order by purchase order id in Coupa.

    Args:
        purchase_order_id: The id of the purchase order.

    Returns:
        The resulting purchase order after using the id to retrieve.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request(resource_name=f"purchase_orders/{purchase_order_id}")
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="Purchase order retrieved successfully.",
        content=coupa_build_purchase_order_from_response(response),
    )
