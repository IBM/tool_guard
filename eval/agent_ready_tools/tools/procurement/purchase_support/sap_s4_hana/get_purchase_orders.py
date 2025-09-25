from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HANAPurchaseOrders:
    """Represents an purchase orders in SAP S4 HANA."""

    purchase_order_id: str
    company_code: str
    created_by_user: str
    supplier_id: str
    date_created: Optional[str] = None
    currency: Optional[str] = None
    purchase_order_type: Optional[str] = None
    purchase_order_date: Optional[str] = None
    payment_terms: Optional[str] = None


@dataclass
class S4HANAPurchaseOrdersResponse:
    """Represents the response from retrieving a list of purchase orders in SAP S4 HANA."""

    purchase_orders: list[S4HANAPurchaseOrders]


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_purchase_orders(
    supplier_id: Optional[str] = None,
    created_by_user: Optional[str] = None,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[S4HANAPurchaseOrdersResponse]:
    """
    Gets a list of the purchase orders from SAP S4 HANA.

    Args:
        supplier_id: The unique identifier of the supplier, returned by the
            `sap_s4_hana_get_suppliers` tool.
        created_by_user: The name of the user that created the purchase order.
        limit: The number of purchase orders to be returned.
        skip: The number of purchase orders to be skipped for pagination.

    Returns:
        A list of purchase orders.
    """
    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    filter_expr = None
    if supplier_id and created_by_user:
        filter_expr = f"Supplier eq '{supplier_id}' and CreatedByUser eq '{created_by_user}'"
    elif supplier_id:
        filter_expr = f"Supplier eq '{supplier_id}'"
    elif created_by_user:
        filter_expr = f"CreatedByUser eq '{created_by_user}'"

    params = {"$top": limit, "$skip": skip}

    response = client.get_request(
        entity="/PurchaseOrder/0001/PurchaseOrder",
        filter_expr=filter_expr,
        params=params,
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    purchase_orders: List[S4HANAPurchaseOrders] = []
    for result in response["response"]["value"]:
        purchase_orders.append(
            S4HANAPurchaseOrders(
                purchase_order_id=result.get("PurchaseOrder", ""),
                company_code=result.get("CompanyCode", ""),
                created_by_user=(result.get("CreatedByUser", "")),
                purchase_order_type=result.get("PurchaseOrderType", ""),
                date_created=(
                    sap_date_to_iso_8601(result.get("CreationDate", ""))
                    if result.get("CreationDate") is not None
                    else None
                ),
                purchase_order_date=(
                    sap_date_to_iso_8601(result.get("PurchaseOrderDate", ""))
                    if result.get("PurchaseOrderDate") is not None
                    else None
                ),
                currency=result.get("DocumentCurrency", ""),
                payment_terms=result.get("PaymentTerms"),
                supplier_id=result.get("Supplier"),
            )
        )
    result = S4HANAPurchaseOrdersResponse(purchase_orders=purchase_orders)
    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
