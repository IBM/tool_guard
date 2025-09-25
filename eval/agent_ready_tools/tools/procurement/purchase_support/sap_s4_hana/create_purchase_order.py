from typing import Any, Dict, List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.common_classes_purchase_support import (
    S4HANAInternationalCommercialTermsTypes,
)
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HanaCreatePurchaseOrderResponse:
    """Represents the response of creating a purchase order in SAP S4 Hana."""

    purchase_order_id: str
    supplier_id: str


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_create_purchase_order(
    supplier_id: str,
    company_code: str,
    purchasing_organization: str,
    purchasing_group: str,
    international_commercial_terms: S4HANAInternationalCommercialTermsTypes,
    material_id: str,
    plant: str,
    purchase_order_quantity_unit: str,
    quantity: int,
    net_price: int,
    document_currency: str,
) -> ToolResponse[S4HanaCreatePurchaseOrderResponse]:
    """
    Creates a purchase order in SAP S4 HANA.

    Args:
        supplier_id: The unique identifier of the supplier, returned by the
            sap_s4_hana_get_suppliers tool.
        company_code: The company code of the supplier.
        purchasing_organization: The purchasing organization of the supplier.
        purchasing_group: The purchasing group for the material in SAP S4 HANA.
        international_commercial_terms: The international commercial terms agreed upon between buyer and seller in SAP S4 HANA.
        material_id: The unique identifier of the material, returned by the
            sap_s4_hana_get_materials tool.
        plant: The plant id associated with the material.
        purchase_order_quantity_unit: The base unit of the material.
        quantity: The required quantity.
        net_price: The net price of the quantity.
        document_currency: The currency of the net_price.

    Returns:
        The result of creating a purchase order.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    # A dictionary that includes the details of the item
    item_details: List[Dict[str, Any]] = [
        {
            "Material": material_id,
            "Plant": plant,
            "PurchaseOrderQuantityUnit": purchase_order_quantity_unit,
            "OrderQuantity": quantity,
            "NetPriceAmount": net_price,
            "DocumentCurrency": document_currency,
        }
    ]

    purchase_order_type = (
        "NB"  # only one standard purchase order type is observed, hence hardcoding the value
    )

    payload: Dict[str, Any] = {
        "PurchaseOrderType": purchase_order_type,
        "Supplier": supplier_id,
        "CompanyCode": company_code,
        "PurchasingOrganization": purchasing_organization,
        "PurchasingGroup": purchasing_group,
        "IncotermsClassification": S4HANAInternationalCommercialTermsTypes[
            international_commercial_terms.upper()
        ].value,
        "_PurchaseOrderItem": item_details,
    }

    response = client.post_request(entity="PurchaseOrder/0001/PurchaseOrder", payload=payload)

    if "error" in response:
        return ToolResponse(
            success=False, message="Request unsuccessful", content=response["error"]["message"]
        )

    if "fault" in response:
        return ToolResponse(
            success=False, message="Request unsuccessful", content=response["fault"]["faultstring"]
        )

    result = S4HanaCreatePurchaseOrderResponse(
        purchase_order_id=response.get("PurchaseOrder", ""),
        supplier_id=response.get("Supplier", ""),
    )

    return ToolResponse(
        success=True,
        message="Purchase order is successfully created",
        content=result,
    )
