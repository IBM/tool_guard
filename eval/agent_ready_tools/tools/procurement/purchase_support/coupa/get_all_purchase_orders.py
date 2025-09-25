from typing import Any, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaPurchaseOrder,
    CoupaPurchaseOrderList,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_helper_functions import (
    coupa_build_purchase_order_from_response,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_all_purchase_orders(
    status: Optional[str] = None,
    supplier_name: Optional[str] = None,
    currency: Optional[str] = None,
    department: Optional[str] = None,
    payment_terms: Optional[str] = None,
    shipping_terms: Optional[str] = None,
    created_by: Optional[str] = None,
    created_at_start: Optional[str] = None,
    created_at_end: Optional[str] = None,
    order_by_direction: str = "desc",
    limit: int = 10,
    offset: int = 0,
) -> ToolResponse[CoupaPurchaseOrderList]:
    """
    Get all purchase orders in Coupa.

    Args:
        status: The status of the purchase order ("issued").
        supplier_name: The name of the supplier to filter by (Grainger (USA)).
        currency: The currency of the purchase order (USD).
        department: Optional. The department of the purchase order (e.g., Operations).
        payment_terms: The payment terms of the purchase order (2/10 Net 30).
        shipping_terms: The shipping terms of the purchase order ("Standard").
        created_by: The user login of the person who created the purchase order.
        created_at_start: The start of the date range for getting purchase orders (YYYY-MM-DD).
        created_at_end: The end of the date range for getting purchase orders (YYYY-MM-DD).
        order_by_direction: The direction in which the purchase orders will be ordered, ("asc" or
            "desc").
        limit: Optional, the count of purchase orders to return - default 10.
        offset: Optional, the number of entries to offset by for pagination - default 0.

    Returns:
        The retrieved list of purchase orders in this Coupa instance.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    # order by created at time
    params: dict[str, Any] = {
        key: value
        for key, value in {
            "limit": limit,
            "offset": offset,
            "order_by": "created-at",
            "dir": order_by_direction,
            "status": status,
            "supplier[name][contains]": supplier_name,
            "currency[code]": currency,
            "requisition-header[department][name]": department,
            "payment-term[code]": payment_terms,
            "shipping-term[code]": shipping_terms,
            "created-by[login]": created_by,
            "created-at[gt]": created_at_start,
            "created-at[lt]": created_at_end,
        }.items()
        if value not in (None, "")
    }

    response = client.get_request_list(resource_name="purchase_orders", params=params)
    if len(response) == 0:
        return ToolResponse(success=False, message="No purchase orders found.")

    if "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    purchase_order_list: List[CoupaPurchaseOrder] = []
    for purchase_order in response:
        purchase_order_list.append(coupa_build_purchase_order_from_response(purchase_order))

    return ToolResponse(
        success=True,
        message="Purchase orders retrieved successfully.",
        content=CoupaPurchaseOrderList(purchase_order_list=purchase_order_list),
    )
