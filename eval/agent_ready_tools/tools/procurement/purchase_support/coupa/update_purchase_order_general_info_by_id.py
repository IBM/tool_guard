from typing import Any, Optional

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
def coupa_update_purchase_order_general_info_by_id(
    purchase_order_id: int,
    # from documentation: can't update other fields while updating exported field
    exported: Optional[bool] = None,
    department: Optional[str] = None,
    ship_to_attention: Optional[str] = None,
    ship_to_user: Optional[str] = None,
    shipping_terms: Optional[str] = None,
    payment_terms: Optional[str] = None,
) -> ToolResponse[CoupaPurchaseOrder]:
    """
    Updates purchase order information from Coupa by ID.

    Args:
        purchase_order_id: The ID of the purchase order in Coupa.
        exported: Optional. The export status of the purchase order (e.g., true or false).
        department: Optional. The department of the purchase order (e.g., Operations).
        ship_to_attention: Optional. The person or department receiving the shipment.
        ship_to_user: Optional. The user login that the order is getting shipped to.
        shipping_terms: Optional. The terms and conditions related to shipping (e.g., "FOB
            Destination").
        payment_terms: Optional. The payment terms agreed upon with the supplier (e.g., "Net 30").

    Returns:
        Boolean indicating whether the purchase order was updated successfully or not.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    payload: dict[str, Any] = {
        key: value
        for key, value in {
            "exported": exported,
            "ship-to-attention": ship_to_attention,
            "department": department,
            "ship-to-user": {"login": ship_to_user} if ship_to_user else None,
            "shipping-term": shipping_terms,
            "payment-term": payment_terms,
        }.items()
        if value not in (None, "")
    }

    response = client.put_request(
        resource_name=f"purchase_orders/{purchase_order_id}", payload=payload
    )
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="Purchase order updated successfully.",
        content=coupa_build_purchase_order_from_response(response),
    )
