from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.purchase_dataclasses import (
    OracleFusionPurchaseOrderHeader,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_get_all_purchase_orders(
    limit: int = 10,
    offset: int = 0,
    po_number: Optional[str] = None,
    supplier_name: Optional[str] = None,
    creation_date_start: Optional[str] = None,
    creation_date_end: Optional[str] = None,
    status: Optional[str] = None,
) -> ToolResponse[List[OracleFusionPurchaseOrderHeader]]:
    """
    Get's all the purchase orders from Oracle Fusion.

    Args:
        limit: Number of purchase orders returned.
        offset: Number of purchase orders to skip for pagination.
        po_number: Number that uniquely identifies the purchase order(e.g., US100000, UK100000).
        supplier_name: The name of the supplier.
        creation_date_start: The start of the date range for getting purchase orders in iso 8601 format(YYYY-MM-DD).
        creation_date_end: The end of the date range for getting purchase orders in iso 8601 format(YYYY-MM-DD).
        status: The status of the purchase order("Canceled","Closed","Closed for Receiving","Closed for Invoicing","Finally Closed","Incomplete","On Hold", "Open","Pending Approval","Pending Change Approval","Pending Funds Reservation","Pending Signature Preparation","Pending Supplier Acknowledgment","Rejected","Sent for Signature","Withdrawn").

    Returns:
        The retrieved list of purchase orders in this Oracle Fusion instance.
    """

    filter_map = {"OrderNumber": po_number, "Supplier": supplier_name, "Status": status}

    expressions = [f"{field}={value}" for field, value in filter_map.items() if value is not None]

    # Handling creation date range

    if creation_date_start and creation_date_end:
        expressions.append(f'CreationDate >= "{creation_date_start}" and <= "{creation_date_end}"')
    elif creation_date_start:
        expressions.append(f'CreationDate >= "{creation_date_start}"')
    elif creation_date_end:
        expressions.append(f'CreationDate <= "{creation_date_end}"')

    query_string = ";".join(expressions) if expressions else None

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params: Dict[str, Any] = {
        "limit": limit,
        "offset": offset,
    }

    if query_string:
        params["q"] = query_string

    params = {key: value for key, value in params.items() if value is not None}

    response = client.get_request(resource_name="purchaseOrders", params=params)

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    if "items" not in response or len(response["items"]) == 0:
        return ToolResponse(success=False, message="No purchase orders returned")

    purchase_orders = []

    for po in response["items"]:
        purchase_orders.append(
            OracleFusionPurchaseOrderHeader(
                purchase_order_id=po.get("POHeaderId", -1),
                po_number=po.get("OrderNumber", ""),
                description=po.get("Description", ""),
                supplier_name=po.get("Supplier", ""),
                ordered_amount=po.get("Ordered", 0),
                currency=po.get("Currency", ""),
                creation_date=po.get("CreationDate", ""),
                status=po.get("Status", ""),
            )
        )

    return ToolResponse(
        success=True,
        message="Returned a list of purchase orders from Oracle Fusion successfully",
        content=purchase_orders,
    )
