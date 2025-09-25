from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.common_classes_purchase_support import (
    SAPS4HANAPurchaseOrderItemTextTypes,
)
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HanaPurchaseOrderItemText:
    """Represents a purchase order item text in SAP S4 HANA."""

    item_text_type: str
    item_text: str


@dataclass
class S4HanaPurchaseOrderItemTextsResponse:
    """A response containing the list of purchase order item texts from SAP S4 HANA."""

    item_texts: list[S4HanaPurchaseOrderItemText]


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_purchase_order_item_texts(
    purchase_order_id: str,
    purchase_order_item_id: str,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[S4HanaPurchaseOrderItemTextsResponse]:
    """
    Gets a list of purchase order item texts.

    Args:
        purchase_order_id: The id of the purchase order returned by the tool
            `sap_s4_hana_get_purchase_orders`.
        purchase_order_item_id: The id of the purchase order item returned by the tool
            `sap_s4_hana_get_purchase_order_items`.
        limit: The number of purchase order item texts returned.
        skip: The number of purchase order item texts to skip for pagination.

    Returns:
        List of purchase order item texts.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {"$top": limit, "$skip": skip}

    response = client.get_request(
        entity=f"PurchaseOrder/0001/PurchaseOrderItem/{purchase_order_id}/{purchase_order_item_id}/_PurchaseOrderItemNote",
        params=params,
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    item_texts: List[S4HanaPurchaseOrderItemText] = []

    for item in response["response"]["value"]:
        item_texts.append(
            S4HanaPurchaseOrderItemText(
                item_text_type=SAPS4HANAPurchaseOrderItemTextTypes(
                    item.get("TextObjectType", "")
                ).name,
                item_text=item.get("PlainLongText", ""),
            )
        )

    result = S4HanaPurchaseOrderItemTextsResponse(item_texts=item_texts)
    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
