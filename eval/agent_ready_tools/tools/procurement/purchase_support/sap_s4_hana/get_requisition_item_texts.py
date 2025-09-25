from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.common_classes_purchase_support import (
    SAPS4HANAItemTextTypes,
)
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HanaRequisitionText:
    """Represents a purchase requisition item text in SAP S4 HANA."""

    item_text_type: str
    item_text: str


@dataclass
class S4HanaRequisitionTextsResponse:
    """A response containing the list of purchase requisition item texts from SAP S4 HANA."""

    requisition_texts: list[S4HanaRequisitionText]


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_requisition_item_texts(
    purchase_requisition_id: str,
    purchase_requisition_item_id: str,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[S4HanaRequisitionTextsResponse]:
    """
    Gets a list of purchase requisition item texts.

    Args:
        purchase_requisition_id: The id of the purchase requisition returned by the tool
            `sap_s4_hana_get_purchase_requisitions`.
        purchase_requisition_item_id: The id of the purchase requisition item returned by the tool
            `'sap_s4_hana_get_purchase_requisition_items`.
        limit: The number of requisition item texts returned.
        skip: The number of requisition item texts to skip for pagination.

    Returns:
        List of purchase requisition item texts.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {"$top": limit, "$skip": skip}

    response = client.get_request(
        entity=f"API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionItem(PurchaseRequisition='{purchase_requisition_id}',PurchaseRequisitionItem='{purchase_requisition_item_id}')/to_PurchaseReqnItemText",
        params=params,
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    requisition_texts: List[S4HanaRequisitionText] = []

    for item in response["response"]["d"]["results"]:
        requisition_texts.append(
            S4HanaRequisitionText(
                item_text_type=SAPS4HANAItemTextTypes(item.get("DocumentText", "")).name,
                item_text=item.get("NoteDescription", ""),
            )
        )

    result = S4HanaRequisitionTextsResponse(requisition_texts=requisition_texts)
    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
