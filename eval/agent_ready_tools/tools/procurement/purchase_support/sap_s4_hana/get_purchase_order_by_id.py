from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.common_classes_purchase_support import (
    SAPS4HANAPurchaseOrderDetails,
)
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_purchase_order_by_id(
    purchase_order_id: str,
) -> ToolResponse[SAPS4HANAPurchaseOrderDetails]:
    """
    Retrieves the general details of a purchase order from SAP S4 HANA.

    Args:
        purchase_order_id: The unique identifier of the purchase order, returned by the
            `sap_s4_hana_get_purchase_orders` tool.

    Returns:
        The general details of the purchase order.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request(entity=f"PurchaseOrder/0001/PurchaseOrder/{purchase_order_id}")

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    item = response["response"]

    purchase_order_details = SAPS4HANAPurchaseOrderDetails(
        purchase_order_number=item.get("PurchaseOrder", ""),
        purchase_order_type=item.get("PurchaseOrderType", ""),
        created_by=item.get("CreatedByUser", ""),
        creation_date=sap_date_to_iso_8601(item.get("CreationDate", "")),
        purchase_order_date=sap_date_to_iso_8601(item.get("PurchaseOrderDate", "")),
        supplier=item.get("Supplier", ""),
        company_code=item.get("CompanyCode", ""),
        purchasing_organization=item.get("PurchasingOrganization", ""),
        purchasing_group=item.get("PurchasingGroup", ""),
        payment_terms=item.get("PaymentTerms", ""),
        document_currency=item.get("DocumentCurrency", ""),
        exchange_rate=float(item.get("ExchangeRate", 0.0)),
    )

    return ToolResponse(
        success=True, message="The data was successfully retrieved", content=purchase_order_details
    )
