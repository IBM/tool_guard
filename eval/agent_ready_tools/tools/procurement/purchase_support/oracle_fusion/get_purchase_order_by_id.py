from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.purchase_dataclasses import (
    OracleFusionPOSupplierDetails,
    OracleFusionPurchaseOrderDetails,
    OracleFusionPurchaseOrderItem,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_get_purchase_order_by_id(
    purchase_order_id: str,
) -> ToolResponse[OracleFusionPurchaseOrderDetails]:
    """
    Gets a purchase order by purchase order id in Oracle Fusion.

    Args:
        purchase_order_id: The id of the purchase order, returned by the `oracle_fusion_get_all_purchase_orders` tool. This ID is
            obtained by applying filters such as the supplier's name, po_number, status or other relevant criteria.

    Returns:
        The resulting purchase order retrieved using the purchase_order_id.
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request(
        resource_name=f"purchaseOrders/{purchase_order_id}", params={"expand": "lines"}
    )

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    line_items = [
        OracleFusionPurchaseOrderItem(
            po_line_id=item.get("POLineId", -1),
            line_number=item.get("LineNumber", -1),
            item_name=item.get("Item", ""),
            item_description=item.get("Description", ""),
            quantity=item.get("Quantity", 0),
            item_value=item.get("Total", 0),
            currency=item.get("Currency", ""),
            unit_of_measure=item.get("PricingUOM", ""),
        )
        for item in response.get("lines", [])
    ]

    supplier_info = OracleFusionPOSupplierDetails(
        supplier_id=response.get("SupplierId", -1),
        supplier_name=response.get("Supplier", ""),
        supplier_site=response.get("SupplierSite", ""),
        supplier_site_id=response.get("SupplierSiteId", -1),
        supplier_contact=response.get("SupplierContact", ""),
        communication_method=response.get("SupplierCommunicationMethod", ""),
        supplier_email=response.get("SupplierEmailAddress", ""),
        supplier_cc_email=response.get("SupplierCCEmailAddress", ""),
        supplier_bcc_email=response.get("SupplierBCCEmailAddress", ""),
        supplier_fax=response.get("SupplierFax", ""),
    )

    purchase_order = OracleFusionPurchaseOrderDetails(
        purchase_order_id=response.get("POHeaderId", -1),
        po_number=response.get("OrderNumber", ""),
        description=response.get("Description", ""),
        status=response.get("Status", ""),
        ordered_amount=response.get("Ordered", 0),
        currency=response.get("Currency", ""),
        supplier_name=response.get("Supplier", ""),
        purchase_basis=response.get("PurchaseBasis", ""),
        sold_to_legal_entity=response.get("SoldToLegalEntity", ""),
        procurement_business_unit=response.get("ProcurementBU", ""),
        bill_to_business_unit=response.get("BillToBU", ""),
        buyer=response.get("Buyer", ""),
        requisition_number=response.get("Requisition", -1),
        tax_amount=response.get("TotalTax", ""),
        shipping_method=response.get("ShippingMethod", ""),
        payment_terms=response.get("PaymentTerms", ""),
        shipping_address=response.get("ShipToLocationAddress", ""),
        billing_address=response.get("BillToLocationAddress", ""),
        creation_date=response.get("CreationDate", ""),
        purchase_order_items=line_items,
        supplier_details=supplier_info,
    )

    return ToolResponse(
        success=True,
        message="Retrieved the purchase order from Oracle Fusion.",
        content=purchase_order,
    )
