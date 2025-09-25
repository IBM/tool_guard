from typing import Any, Dict

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.ariba_client import get_ariba_client
from agent_ready_tools.clients.clients_enums import AribaApplications
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import ARIBA_BUYER_CONNECTIONS


@dataclass
class AribaPurchaseOrderHeaderDetails:
    """Represents the general details of a Purchase Order in SAP Ariba."""

    purchase_order_num: str
    supplier_name: str
    customer_name: str
    po_amount: float
    po_currency: str
    po_status: str
    created_date: str
    order_date: str
    po_ship_to_street: str
    po_ship_to_city: str
    po_ship_to_state: str


@tool(expected_credentials=ARIBA_BUYER_CONNECTIONS)
def ariba_get_purchase_order_details_by_id(
    purchase_order_num: str,
) -> ToolResponse[AribaPurchaseOrderHeaderDetails]:
    """
    Gets the purchase order details from purchase order number in SAP Ariba.

    Args:
        purchase_order_num: documentNumber of the purchase order.

    Returns:
        The resulting purchase order details retrieved using the purchase_order_num.
    """

    try:
        client = get_ariba_client(application=AribaApplications.BUYER)
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    params: Dict[str, Any] = {}
    params["$filter"] = f"documentNumber eq '{purchase_order_num}'"

    endpoint = f"purchase-orders/v1/prod/orders"

    response = client.get_request(
        endpoint=endpoint,
        params=params,
    )

    if "error" in response or "message" in response:
        content = response.get("message", "")
        return ToolResponse(
            success=False,
            message=f"Request unsuccessful {content}",
        )

    content_list = response.get("content", [])

    if not content_list:
        return ToolResponse(
            success=True, message=f"There was no purchase order with id {purchase_order_num}"
        )

    po_details = None
    if content_list:
        po = content_list[0]

        po_details = AribaPurchaseOrderHeaderDetails(
            purchase_order_num=po.get("documentNumber", ""),
            supplier_name=po.get("supplierName", ""),
            customer_name=po.get("customerName", ""),
            po_amount=(po.get("poAmount") or {}).get("amount", 0),
            po_currency=(po.get("poAmount") or {}).get("currencyCode", ""),
            po_status=po.get("status", ""),
            created_date=po.get("created", ""),
            order_date=po.get("orderDate", ""),
            po_ship_to_street=po.get("poShipToStreet", ""),
            po_ship_to_city=po.get("poShipToCity", ""),
            po_ship_to_state=po.get("poShipToState", ""),
        )

    return ToolResponse(
        success=True,
        message="The data was successfully retrieved",
        content=po_details,
    )
