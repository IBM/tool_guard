from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.common_classes_purchase_support import (
    SAPS4HANAPurchaseOrderLineItem,
)
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_purchase_order_items(
    purchase_order_id: str,
) -> ToolResponse[List[SAPS4HANAPurchaseOrderLineItem]]:
    """
    Retrieves the line items of a purchase order from SAP S4 HANA.

    Args:
        purchase_order_id: The unique identifier of the purchase order, returned by the
            `sap_s4_hana_get_purchase_orders` tool.

    Returns:
        A list of purchase order line items in SAP S4 HANA.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request(
        entity=f"PurchaseOrder/0001/PurchaseOrder/{purchase_order_id}/_PurchaseOrderItem"
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    items = response["response"].get("value", [])

    purchase_order_items = [
        SAPS4HANAPurchaseOrderLineItem(
            purchase_order=item.get("PurchaseOrder", ""),
            purchase_order_item=item.get("PurchaseOrderItem", ""),
            material=item.get("Material", ""),
            order_quantity=float(item.get("OrderQuantity", 0.0)),
            net_price_amount=float(item.get("NetPriceAmount", 0.0)),
            net_amount=float(item.get("NetAmount", 0.0)),
            document_currency=item.get("DocumentCurrency", ""),
            plant=item.get("Plant", ""),
        )
        for item in items
    ]
    result = purchase_order_items
    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
