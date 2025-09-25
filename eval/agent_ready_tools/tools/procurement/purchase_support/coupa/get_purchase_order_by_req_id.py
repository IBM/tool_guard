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
def coupa_get_purchase_order_by_req_id(
    requisition_id: int,
) -> ToolResponse[CoupaPurchaseOrder]:
    """
    Gets a purchase order by requisition id in Coupa.

    Args:
        requisition_id: The id of the requisition.

    Returns:
        The resulting purchase order object if the query returns a result, otherwise an empty list.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request_list(
        resource_name="purchase_orders",
        params={"requisition-header[id]": requisition_id},
    )
    if len(response) == 0:
        return ToolResponse(success=False, message="No purchase order found.")

    if "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    # query returns list of one dictionary if response is nonempty, otherwise return the empty query
    return ToolResponse(
        success=True,
        message="Purchase order retrieved successfully",
        content=coupa_build_purchase_order_from_response(response[0]),
    )
