from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.watson_commerce_client import get_watson_commerce_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.supply_chain.ibm_sip.inventory_reallocation.common_dataclasses import (
    SIPInventoryItemSupply,
)
from agent_ready_tools.utils.tool_credentials import WATSON_COMMERCE_CONNECTIONS


@tool(expected_credentials=WATSON_COMMERCE_CONNECTIONS)
def ibm_sip_get_item_supplies(
    item_id: str,
    ship_node: str,
    uom: str = "EACH",
) -> ToolResponse[list[SIPInventoryItemSupply]]:
    """
    Searches for an item in a ship node.

    Args:
        item_id: ID of the Item
        ship_node: The ship node associated with the supply.
        uom: The unit of measure in the context of the item's quantity. For example, 1 DOZEN egg or 2.7 YARD of fabric.

    Returns:
        The matched supplies.
    """
    try:
        client = get_watson_commerce_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {
        k: v
        for k, v in {"itemId": item_id, "unitOfMeasure": uom, "shipNode": ship_node}.items()
        if v not in (None, "", "null")
    }

    response = client.get_request(resource_name="/v1/supplies", params=params)
    if "errorMessage" in response:
        return ToolResponse(success=False, message=response["errorMessage"])

    assert isinstance(response, list)

    if len(response) == 0:
        return ToolResponse(success=False, message=f"No supplies were found for item {item_id}")

    result = [
        SIPInventoryItemSupply(
            item_id=r.get("itemId"),
            item_type=r.get("type"),
            unit_of_measure=r.get("unitOfMeasure"),
            quantity=r.get("quantity", 0.0),
            ship_node=r.get("shipNode"),
            segment=r.get("segment"),
            segment_type=r.get("segmentType"),
            eta=r.get("eta"),
            ship_by_date=r.get("shipByDate"),
        )
        for r in response
    ]

    return ToolResponse(
        success=True, message=f"Following is the list of supplies for {item_id}", content=result
    )
