from typing import Any

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.common_classes_purchase_support import (
    SAPS4HANAItemTextTypes,
)
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class SAPS4HANAAddRequisitionItemTextResult:
    """Represents the result of adding the text for requisition item in SAP Hana."""

    item_text: str


LANGUAGE = "EN"  # Defaulting Language to english.


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_add_requisition_item_text(
    purchase_requisition_id: str,
    purchase_requisition_item_id: str,
    item_text: str,
    item_text_types: SAPS4HANAItemTextTypes,
) -> ToolResponse[SAPS4HANAAddRequisitionItemTextResult]:
    """
    Adding the text for requisition item in SAP S4 Hana.

    Args:
        purchase_requisition_id: The id of the purchase requisition returned by the tool
            `sap_s4_hana_get_purchase_requisitions`.
        purchase_requisition_item_id: The id of the purchase requisition item returned by the tool
            `sap_s4_hana_get_purchase_requisition_items`.
        item_text: The text of the purchase requisition item.
        item_text_types: The item text types of a purchase requisition in SAP S4 HANA.

    Returns:
        Result from adding the text for requisition item
    """
    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    payload: dict[str, Any] = {
        "PurchaseRequisition": purchase_requisition_id,
        "PurchaseRequisitionItem": purchase_requisition_item_id,
        "NoteDescription": item_text,
        "DocumentText": SAPS4HANAItemTextTypes[item_text_types.upper()].value,
        "Language": LANGUAGE,
    }

    response = client.post_request(
        entity=f"API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionItem(PurchaseRequisition='{purchase_requisition_id}',PurchaseRequisitionItem='{purchase_requisition_item_id}')/to_PurchaseReqnItemText",
        payload=payload,
    )
    if "error" in response:
        return ToolResponse(
            success=False, message="Request unsuccessful", content=response["error"]["message"]
        )

    if "fault" in response:
        return ToolResponse(
            success=False, message="Request unsuccessful", content=response["fault"]["faultstring"]
        )

    result = SAPS4HANAAddRequisitionItemTextResult(item_text=item_text)
    return ToolResponse(
        success=True,
        message="Requisition item text is successfully added",
        content=result,
    )
