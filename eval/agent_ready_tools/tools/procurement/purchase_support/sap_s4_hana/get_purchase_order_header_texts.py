from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.common_classes_purchase_support import (
    SAPS4HANAPurchaseOrderHeaderTextTypes,
)
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HanaPurchaseOrderHeaderText:
    """Represents a purchase order header text in SAP S4 HANA."""

    header_text_type: str
    header_text: str


@dataclass
class S4HanaPurchaseOrderHeaderTextsResponse:
    """A response containing the list of purchase order header texts from SAP S4 HANA."""

    header_texts: list[S4HanaPurchaseOrderHeaderText]


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_purchase_order_header_texts(
    purchase_order_id: str,
    header_text_type: Optional[SAPS4HANAPurchaseOrderHeaderTextTypes] = None,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[S4HanaPurchaseOrderHeaderTextsResponse]:
    """
    Gets a list of purchase order header texts.

    Args:
        purchase_order_id: The id of the purchase order returned by the tool
            `sap_s4_hana_get_purchase_orders`.
        header_text_type: The type of the header text.
        limit: The number of purchase order header texts returned.
        skip: The number of purchase order header texts to skip for pagination.

    Returns:
        List of purchase order header texts.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    filter_expr = None
    if header_text_type:
        filter_expr = f"TextObjectType eq '{header_text_type}'"

    params = {"$top": limit, "$skip": skip}

    response = client.get_request(
        entity=f"PurchaseOrder/0001/PurchaseOrder/{purchase_order_id}/_PurchaseOrderNote",
        filter_expr=filter_expr,
        params=params,
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    header_texts: List[S4HanaPurchaseOrderHeaderText] = []

    for header in response["response"]["value"]:
        header_texts.append(
            S4HanaPurchaseOrderHeaderText(
                header_text_type=SAPS4HANAPurchaseOrderHeaderTextTypes(
                    header.get("TextObjectType", "")
                ).name,
                header_text=header.get("PlainLongText", ""),
            )
        )

    result = S4HanaPurchaseOrderHeaderTextsResponse(header_texts=header_texts)
    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
