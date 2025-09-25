from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_update_purchase_requisition_item(
    purchase_requisition_id: str,
    purchase_requisition_item_id: str,
    item_text: Optional[str] = None,
    requested_quantity: Optional[str] = None,
    price: Optional[str] = None,
    delivery_date: Optional[str] = None,
    material: Optional[str] = None,
    material_group: Optional[str] = None,
    plant: Optional[str] = None,
    company_code: Optional[str] = None,
    purchasing_group: Optional[str] = None,
    purchasing_organization: Optional[str] = None,
    currency: Optional[str] = None,
    requisitioner_name: Optional[str] = None,
    supplier: Optional[str] = None,
) -> ToolResponse:
    """
    Updates a purchase requisition item in SAP S4 HANA.

    Args:
        purchase_requisition_id: The id of the purchase requisition returned by `sap_s4_hana_get_purchase_requisitions` tool.
        purchase_requisition_item_id: The item ID within the purchase requisition returned by `sap_s4_hana_get_purchase_requisition_items` tool.
        item_text: Description or note for the item.
        requested_quantity: The quantity of items requested.
        price: Unit price of the requested material or service.
        delivery_date: Expected date for the item to be delivered.
        material: The id of the material, retrieved by the sap_s4_hana_get_materials tool.
        material_group: The id of the material group, retrieved by the sap_s4_hana_get_materials tool.
        plant: The production plant of the material.
        company_code: The company code associated with the item within the purchase requisition.
        purchasing_group: The purchasing group for the material.
        purchasing_organization: The purchasing organization of the material.
        currency: A three letter code representing the currency, example: INR, USD.
        requisitioner_name: The name of the requisitioner.
        supplier: The ID of the supplier associated with the item within the purchase requisition.

    Returns:
        The HTTP status code of the update response.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    payload = {
        "PurchaseRequisitionItemText": item_text,
        "RequestedQuantity": requested_quantity,
        "PurchaseRequisitionPrice": price,
        "DeliveryDate": sap_date_to_iso_8601(delivery_date) if delivery_date else None,
        "Material": material,
        "MaterialGroup": material_group,
        "Plant": plant,
        "CompanyCode": company_code,
        "PurchasingGroup": purchasing_group,
        "PurchasingOrganization": purchasing_organization,
        "PurReqnItemCurrency": currency,
        "RequisitionerName": requisitioner_name,
        "Supplier": supplier,
    }

    payload = {key: value for key, value in payload.items() if value}

    response_code = client.patch_request(
        entity=(
            f"API_PURCHASEREQ_PROCESS_SRV/"
            f"A_PurchaseRequisitionItem(PurchaseRequisition='{purchase_requisition_id}',"
            f"PurchaseRequisitionItem='{purchase_requisition_item_id}')"
        ),
        payload=payload,
    )
    if "error" in response_code:
        return ToolResponse(
            success=False, message="Request unsuccessful", content=response_code["error"]["message"]
        )

    if "fault" in response_code:
        return ToolResponse(
            success=False,
            message="Request unsuccessful",
            content=response_code["fault"]["faultstring"],
        )

    result = response_code
    return ToolResponse(
        success=True,
        message="The data was successfully updated",
        content=result,
    )
