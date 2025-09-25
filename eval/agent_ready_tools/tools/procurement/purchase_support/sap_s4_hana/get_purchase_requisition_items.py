from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HanaPurchaseRequisitionItems:
    """Represents a purchase requisition item in SAP S4 HANA."""

    purchase_requisition_item_id: str
    purchasing_group: str
    purchasing_organization: str
    plant: str
    material: str
    material_group: str
    creation_date: str
    delivery_date: str
    release_date: str
    currency: str
    requested_quantity: str
    price: str
    net_amount: str
    requisitioner_name: str
    base_unit: str
    postal_code: str
    city: str
    country: str
    region: str


@dataclass
class S4HanaPurchaseRequisitionItemsResponse:
    """Represents a purchase requisition items in SAP S4 HANA."""

    purchase_requisition_items: list[S4HanaPurchaseRequisitionItems]


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_purchase_requisition_items(
    purchase_requisition_id: str,
) -> ToolResponse[S4HanaPurchaseRequisitionItemsResponse]:
    """
    Gets the purchase requisition items details.

    Args:
        purchase_requisition_id: The id of the purchase requisition, returned by the
            `sap_s4_hana_get_purchase_requisitions`.

    Returns:
        The purchase requisition items details.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request(
        entity=f"API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionHeader('{purchase_requisition_id}')",
        expand_expr="to_PurchaseReqnItem,to_PurchaseReqnItem/to_PurchaseReqnDeliveryAddress",
    )
    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    result = response["response"]["d"]

    purchase_requisition_items = []

    for item in result["to_PurchaseReqnItem"]["results"]:

        purchase_requisition_items.append(
            S4HanaPurchaseRequisitionItems(
                purchase_requisition_item_id=item.get("PurchaseRequisitionItem", ""),
                purchasing_group=item.get("PurchasingGroup", ""),
                purchasing_organization=item.get("PurchasingOrganization", ""),
                plant=item.get("Plant", ""),
                material=item.get("Material", ""),
                material_group=item.get("MaterialGroup", ""),
                creation_date=(
                    sap_date_to_iso_8601(item.get("CreationDate", ""))
                    if item.get("CreationDate", "")
                    else ""
                ),
                delivery_date=(
                    sap_date_to_iso_8601(item.get("DeliveryDate", ""))
                    if item.get("DeliveryDate", "")
                    else ""
                ),
                release_date=(
                    sap_date_to_iso_8601(item.get("PurchaseRequisitionReleaseDate", ""))
                    if item.get("PurchaseRequisitionReleaseDate", "")
                    else ""
                ),
                currency=item.get("PurReqnItemCurrency", ""),
                requested_quantity=item.get("RequestedQuantity", ""),
                price=item.get("PurchaseRequisitionPrice", ""),
                net_amount=item.get("ItemNetAmount", ""),
                requisitioner_name=item.get("RequisitionerName", ""),
                base_unit=item.get("BaseUnit", ""),
                postal_code=item.get("to_PurchaseReqnDeliveryAddress", {}).get("PostalCode", ""),
                city=item.get("to_PurchaseReqnDeliveryAddress", {}).get("CityName", ""),
                country=item.get("to_PurchaseReqnDeliveryAddress", {}).get("Country", ""),
                region=item.get("to_PurchaseReqnDeliveryAddress", {}).get("Region", ""),
            )
        )

    result = S4HanaPurchaseRequisitionItemsResponse(
        purchase_requisition_items=purchase_requisition_items,
    )
    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
