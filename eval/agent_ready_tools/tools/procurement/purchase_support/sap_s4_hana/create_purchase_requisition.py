from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.common_classes_purchase_support import (
    SAPS4HANAAccountAssignmentCategory,
)
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HANACreatePurchaseRequisitionResponse:
    """Represents the response from creating a purchase requisition in SAP S4 HANA."""

    purchase_requisition_id: str


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_create_purchase_requisition(
    account_assignment_category: SAPS4HANAAccountAssignmentCategory,
    material_id: str,
    requested_quantity: str,
    purchase_requisition_price: str,
    purchasing_group: str,
    plant: str,
    purchase_requisition_item: Optional[str] = None,
    requisitioner_name: Optional[str] = None,
    supplier_id: Optional[str] = None,
    purchase_requisition_description: Optional[str] = None,
    gl_account: Optional[str] = None,
    order_id: Optional[str] = None,
    sales_order: Optional[str] = None,
    sales_document_item: Optional[str] = None,
    wbse_element: Optional[str] = None,
) -> ToolResponse[S4HANACreatePurchaseRequisitionResponse]:
    """
    Creates a requisition in SAP S4 HANA.

    Args:
        account_assignment_category: The assignment category of the purchase requisition in SAP S4 HANA.
        material_id: The id of the material, retrieved by the sap_s4_hana_get_materials tool.
        requested_quantity: The quantity of material being requested in the purchase requisition.
        purchase_requisition_price: The price of the purchase requisition.
        purchasing_group: The purchasing group for the material in SAP S4 HANA.
        plant: The production plant of the material.
        purchase_requisition_item: The unique identifier for the purchase requisition item.
        requisitioner_name: The name of the purchase requisitioner.
        supplier_id: The id of the supplier, retrieved by the sap_s4_hana_get_suppliers tool.
        purchase_requisition_description: A brief description for the purchase requisition.
        gl_account: The GL account number associated with the purchase requisition.
        order_id: The order ID when Account Assignment Category is 'ORDER' or 'COST_CENTRE'.
        sales_order: The sales order number associated with the purchase requisition when Account
            Assignment Category is 'SALES_ORDER'.
        sales_document_item: The sales document item number associated to the sales order.
        wbse_element: The WBS element associated with the purchase requisition when Account
            Assignment Category is 'PROJECT'.

    Returns:
        The result from executing the sap_s4_hana_create_requisition tool in SAP S4 HANA.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    payload: dict[str, Any] = {"PurReqnDescription": purchase_requisition_description}
    payload = {key: value for key, value in payload.items() if value}

    item_payload: dict[str, Any] = {
        "to_PurchaseReqnItem": {
            "results": [
                {
                    "PurchaseRequisitionType": "NB",
                    "PurchaseRequisitionItem": purchase_requisition_item,
                    "AccountAssignmentCategory": SAPS4HANAAccountAssignmentCategory[
                        account_assignment_category.upper()
                    ].value,
                    "Material": material_id,
                    "PurchasingGroup": purchasing_group,
                    "RequestedQuantity": requested_quantity,
                    "PurchaseRequisitionPrice": purchase_requisition_price,
                    "Plant": plant,
                    "Supplier": supplier_id,
                    "RequisitionerName": requisitioner_name,
                }
            ]
        }
    }

    filtered_item_payload: list[dict[str, str | None]] = [
        {key: value for key, value in item.items() if value}
        for item in item_payload.get("to_PurchaseReqnItem", {}).get("results", [])
        if any(item.values())
    ]

    item_payload = {"to_PurchaseReqnItem": {"results": filtered_item_payload}}
    payload["to_PurchaseReqnItem"] = item_payload.get("to_PurchaseReqnItem", {"results": []})

    account_assignment_category_enum = SAPS4HANAAccountAssignmentCategory[
        account_assignment_category.upper()
    ]
    account_assignment_category_str = account_assignment_category_enum.value

    item_data = payload.get("to_PurchaseReqnItem", {}).get("results", [{}])[0]

    if account_assignment_category_str != "U":
        item_data["to_PurchaseReqnAcctAssgmt"] = {"results": []}

        if account_assignment_category_str in ["F", "K"]:
            item_data["to_PurchaseReqnAcctAssgmt"]["results"].append(
                {"GLAccount": gl_account, "OrderID": order_id}
            )

        elif account_assignment_category_str == "C":
            item_data["to_PurchaseReqnAcctAssgmt"]["results"].append(
                {
                    "GLAccount": gl_account,
                    "SalesOrder": sales_order,
                    "SalesDocumentItem": sales_document_item,
                }
            )

        elif account_assignment_category_str == "P":
            item_data["to_PurchaseReqnAcctAssgmt"]["results"].append(
                {"GLAccount": gl_account, "WBSElement": wbse_element}
            )

    response = client.post_request(
        entity="API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionHeader", payload=payload
    )

    if "error" in response:
        return ToolResponse(
            success=False, message="Request unsuccessful", content=response["error"]["message"]
        )

    if "fault" in response:
        return ToolResponse(
            success=False, message="Request unsuccessful", content=response["fault"]["faultstring"]
        )

    purchase_requisition_id = response.get("d", {}).get("PurchaseRequisition", "")

    result = S4HANACreatePurchaseRequisitionResponse(
        purchase_requisition_id=purchase_requisition_id
    )

    return ToolResponse(
        success=True,
        message="Purchase requisition is successfully created",
        content=result,
    )
