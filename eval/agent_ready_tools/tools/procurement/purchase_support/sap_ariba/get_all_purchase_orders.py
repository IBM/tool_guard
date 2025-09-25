from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.ariba_client import get_ariba_client
from agent_ready_tools.clients.clients_enums import AribaApplications
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import ARIBA_BUYER_CONNECTIONS


@dataclass
class AribaPurchaseOrderDetails:
    """Represents the general details of a Purchase Order in SAP Ariba."""

    purchase_order_num: str
    supplier_name: str
    customer_name: str
    po_amount: float
    po_currency: str
    po_status: str
    order_date: str
    po_ship_to_code: str


@dataclass
class AribaPurchaseOrderDetailsResults:
    """Represents the response from getting all PO Buyer in SAP Ariba."""

    po_details_result: List[AribaPurchaseOrderDetails]


@tool(expected_credentials=ARIBA_BUYER_CONNECTIONS)
def ariba_get_all_purchase_order_details(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    supplier_an_id: Optional[str] = None,
) -> ToolResponse[AribaPurchaseOrderDetailsResults]:
    """
    Gets the purchase order details from Ariba.

    Args:
        start_date: The start date of the purchase order in ISO 8601 format (e.g., YYYY-MM-DDTHH:MM:SS).
        end_date: The end date of the purchase order in ISO 8601 format (e.g., YYYY-MM-DDTHH:MM:SS).
        supplier_an_id: The AN id of the supplier, returned by the ariba_get_suppliers tool.

    Returns:
        retrieve the purchase order details.
    """

    try:
        client = get_ariba_client(application=AribaApplications.BUYER)
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    params: Dict[str, Any] = {}
    filters = []

    if start_date:
        filters.append(f"startDate eq '{start_date}'")
    if end_date:
        filters.append(f"endDate eq '{end_date}'")
    if supplier_an_id:
        filters.append(f"supplierANID eq '{supplier_an_id}'")

    if filters:
        params["$filter"] = " and ".join(filters)

    endpoint = f"purchase-orders/v1/prod/orders"

    response = client.get_request(endpoint=endpoint, params=params)

    if "error" in response or "message" in response:
        content = response.get("message", "")
        return ToolResponse(
            success=False,
            message=f"Request unsuccessful {content}",
        )

    po_details: List[AribaPurchaseOrderDetails] = []

    for supplier in response["content"]:
        if supplier.get("documentNumber"):
            po_details.append(
                AribaPurchaseOrderDetails(
                    purchase_order_num=supplier.get("documentNumber", ""),
                    supplier_name=supplier.get("supplierName", ""),
                    customer_name=supplier.get("customerName", ""),
                    po_amount=(supplier.get("poAmount") or {}).get("amount", 0),
                    po_currency=(supplier.get("poAmount") or {}).get("currencyCode", ""),
                    po_status=supplier.get("status", ""),
                    order_date=supplier.get("orderDate", ""),
                    po_ship_to_code=supplier.get("poShipToCode", ""),
                )
            )
    return ToolResponse(
        success=True,
        message="The data was successfully retrieved",
        content=AribaPurchaseOrderDetailsResults(po_details_result=po_details),
    )
