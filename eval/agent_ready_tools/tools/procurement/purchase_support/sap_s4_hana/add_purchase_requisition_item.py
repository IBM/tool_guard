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
class S4HANAAddRequisitionItemResponse:
    """Represents the result of adding purchase requisition item in SAP S4 HAHA."""

    purchase_requisition_id: str
    purchase_requisition_item_id: str


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_add_purchase_requisition_item(
    purchase_requisition_id: str,
    account_assignment_category: SAPS4HANAAccountAssignmentCategory,
    material_id: str,
    plant: str,
    purchasing_group: str,
    requested_quantity: str,
    purchase_requisition_price: str,
    gl_account: Optional[str] = None,
    order_id: Optional[str] = None,
    sales_order: Optional[str] = None,
    sales_document_item: Optional[str] = None,
    wbse_element: Optional[str] = None,
) -> ToolResponse[S4HANAAddRequisitionItemResponse]:
    """
    Adds an item to a purchase requisition in SAP S4 HANA.

    Args:
        purchase_requisition_id: The id of the purchase requisition, returned by
            sap_s4_hana_get_purchase_requisitions tool.
        account_assignment_category: The assignment category of the purchase requisition in SAP S4
            HANA.
        material_id: The id of the material, retrieved by the sap_s4_hana_get_materials tool.
        plant: The production plant of the material.
        purchasing_group: The purchasing group for the material in SAP S4 HANA.
        requested_quantity: The quantity of material being requested in the purchase requisition.
        purchase_requisition_price: The price of the purchase requisition.
        gl_account: The GL account number associated with the purchase requisition.
        order_id: The order ID when Account Assignment Category is 'ORDER' or 'COST_CENTRE'.
        sales_order: The sales order number associated with the purchase requisition when Account
            Assignment Category is 'SALES_ORDER'.
        sales_document_item: The sales document item number associated to the sales order.
        wbse_element: The WBS element associated with the purchase requisition when Account
            Assignment Category is 'PROJECT'.

    Returns:
        The result from executing the sap_s4_hana_add_purchase_requisition_item tool in SAP S4 HANA.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    payload: dict[str, Any] = {
        "PurchaseRequisition": purchase_requisition_id,
        "AccountAssignmentCategory": SAPS4HANAAccountAssignmentCategory[
            account_assignment_category.upper()
        ].value,
        "Material": material_id,
        "Plant": plant,
        "PurchasingGroup": purchasing_group,
        "RequestedQuantity": requested_quantity,
        "PurchaseRequisitionPrice": purchase_requisition_price,
        "to_PurchaseReqnItemText": {
            "results": [
                {
                    "Language": "EN",
                }
            ]
        },
    }

    account_assignment_category_enum = SAPS4HANAAccountAssignmentCategory[
        account_assignment_category.upper()
    ]
    account_assignment_category_str = account_assignment_category_enum.value

    if account_assignment_category_str != "U":
        payload["to_PurchaseReqnAcctAssgmt"] = {"results": []}
        if account_assignment_category_str in ["F", "K"]:
            payload["to_PurchaseReqnAcctAssgmt"]["results"].append(
                {"GLAccount": gl_account, "OrderID": order_id}
            )
        elif account_assignment_category_str == "C":
            payload["to_PurchaseReqnAcctAssgmt"]["results"].append(
                {
                    "GLAccount": gl_account,
                    "SalesOrder": sales_order,
                    "SalesDocumentItem": sales_document_item,
                }
            )
        elif account_assignment_category_str == "P":
            payload["to_PurchaseReqnAcctAssgmt"]["results"].append(
                {"GLAccount": gl_account, "WBSElement": wbse_element}
            )

    payload = {
        key: (
            {key: value for key, value in value.items() if value}
            if isinstance(value, dict)
            else value
        )
        for key, value in payload.items()
        if value
    }

    response = client.post_request(
        entity="API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionItem", payload=payload
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
    purchase_requisition_item_id = response.get("d", {}).get("PurchaseRequisitionItem", "")

    result = S4HANAAddRequisitionItemResponse(
        purchase_requisition_id=purchase_requisition_id,
        purchase_requisition_item_id=purchase_requisition_item_id,
    )

    return ToolResponse(
        success=True,
        message="Purchase requisition successfully added",
        content=result,
    )
