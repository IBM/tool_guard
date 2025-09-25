from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.purchase_dataclasses import (
    OracleFusionRequisitionCartItems,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_get_requisition_cart_items(
    category: Optional[str] = None,
    item_number: Optional[str] = None,
    item_description: Optional[str] = None,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
) -> ToolResponse[List[OracleFusionRequisitionCartItems]]:
    """
    Gets the items available in cart for requisition in Oracle Fusion.

    Args:
        category: The name of the item category.
        item_number: The number of the item.
        item_description: The description of the item.
        limit: Number of items returned.
        offset: Number of items to skip for pagination.

    Returns:
        List of available items in the cart.
    """

    filter_map = {"Item ": item_number, "Category": category}

    expressions = [f"{field}={value}" for field, value in filter_map.items() if value is not None]

    if item_description:
        expressions.append(f"Description LIKE '%{item_description}%'")

    query_string = ";".join(expressions) if expressions else None

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params: Dict[str, Any] = {
        "limit": limit,
        "offset": offset,
    }

    if query_string:
        params["q"] = query_string

    response = client.get_request(resource_name="purchaseAgreementLines", params=params)

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    if "items" not in response or len(response["items"]) == 0:
        return ToolResponse(success=False, message="No cart items returned")

    cart_items = []

    for item in response["items"]:
        cart_items.append(
            OracleFusionRequisitionCartItems(
                item_number=item.get("Item", ""),
                item_description=item.get("Description", ""),
                category=item.get("Category", ""),
                unit_of_measure=item.get("UOM", ""),
                unit_price=item.get("Price", 0),
                currency_code=item.get("CurrencyCode", ""),
                line_type=item.get("LineType", ""),
            )
        )

    return ToolResponse(
        success=True,
        message="Returned list of cart items from Oracle Fusion successfully",
        content=cart_items,
    )
