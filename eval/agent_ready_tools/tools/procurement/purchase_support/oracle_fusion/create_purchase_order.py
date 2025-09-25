from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.purchase_dataclasses import (
    OracleFusionCreatePurchaseOrderResult,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_create_purchase_order(
    procurement_business_unit_id: int,
    requisitioning_business_unit: str,
    buyer_email: str,
    currency_code: str,
    pay_on_receipt: Optional[bool] = False,
    buyer_managed_transport: Optional[bool] = True,
    supplier_id: Optional[int] = None,
    supplier_site_id: Optional[int] = None,
    special_handling_type_code: Optional[str] = None,
    default_ship_to_location_id: Optional[int] = None,
) -> ToolResponse[OracleFusionCreatePurchaseOrderResult]:
    """
    Creates a purchase order in Orcale fusion.

    Args:
        procurement_business_unit_id: The unique identifier of the procurement business unit, returned by the `oracle_fusion_get_procurement_business_units` tool.
        requisitioning_business_unit: The name of the requisitioning business unit.
        buyer_email: The email address of the buyer.
        currency_code: The code of the transaction currency, returned by the `oracle_fusion_get_currencies` tool.
        pay_on_receipt: Indicates whether payment is triggered upon receipt of goods. Defaults to False.
        buyer_managed_transport: Indicates if the buyer manages transportation. Defaults to True.
        supplier_id: The id of the supplier, returned by the `oracle_fusion_get_all_suppliers` tool. This ID is obtained by applying filters such as the supplier's name, number, or other relevant criteria.
        supplier_site_id: The id of a supplier site, obtained by calling the `oracle_fusion_get_supplier_sites` tool using the supplier_id.
        special_handling_type_code: The code indicating special handling requirements, returned by the `oracle_fusion_get_special_handling_types` tool.
        default_ship_to_location_id: The ID of the default shipping location, returned by the `oracle_fusion_get_ship_to_locations` tool.

    Returns:
        A ToolResponse object containing the API response or an error message.
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    payload = {
        "ProcurementBUId": procurement_business_unit_id,
        "RequisitioningBU": requisitioning_business_unit,
        "BuyerEmail": buyer_email,
        "CurrencyCode": currency_code,
        "PayOnReceiptFlag": pay_on_receipt,
        "BuyerManagedTransportFlag": buyer_managed_transport,
        "SupplierId": supplier_id,
        "SupplierSiteId": supplier_site_id,
        "SpecialHandlingTypeCode": special_handling_type_code,
        "DefaultShipToLocationId": default_ship_to_location_id,
    }

    payload = {key: value for key, value in payload.items() if value is not None}

    response = client.post_request(resource_name=f"draftPurchaseOrders", payload=payload)

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    purchase_order_details = OracleFusionCreatePurchaseOrderResult(
        purchase_order_id=response.get("POHeaderId", -1),
        purchase_order_number=response.get("OrderNumber", ""),
        procurement_business_unit=response.get("ProcurementBU", ""),
        requisitioning_business_unit=response.get("RequisitioningBU", ""),
        buyer_email=response.get("BuyerEmail", ""),
        currency=response.get("Currency", ""),
        supplier=response.get("Supplier", ""),
        supplier_site=response.get("SupplierSite", ""),
        special_handling_type=response.get("SpecialHandlingType", ""),
        default_ship_to_location=response.get("DefaultShipToLocation", ""),
    )

    return ToolResponse(
        success=True,
        message="Created purchase order in Oracle Fusion.",
        content=purchase_order_details,
    )
