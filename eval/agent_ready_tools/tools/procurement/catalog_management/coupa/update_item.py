from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.catalog_management.coupa.get_item_by_id import (
    CoupaItemDetails,
)
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_update_item(
    item_id: int,
    name: Optional[str] = None,
    item_number: Optional[str] = None,
    description: Optional[str] = None,
    item_type: Optional[str] = None,
) -> ToolResponse[CoupaItemDetails]:
    """
    Updates specific fields (name, item_number, description, item_type) for an existing item in
    Coupa.

    Args:
        item_id: The Coupa internal ID of the item to update (required).
        name: The new name for the item (optional, default=None).
        item_number: The new item number/SKU for the item (optional, default=None).
        description: The new description for the item (optional, default=None).
        item_type: The new type for the item (e.g., "Item", "Service") (optional, default=None).

    Returns:
        The updated item details.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failed to retrieve credentials.")

    # --- Construct the Payload ---
    # Only include fields that are explicitly provided for update
    payload: Dict[str, Any] = {}

    if name is not None:
        payload["name"] = name
    if item_number is not None:
        payload["item-number"] = item_number
    if description is not None:
        payload["description"] = description
    if item_type is not None:
        payload["item-type"] = item_type

    params = {"fields": '["id", "item-number", "name", "description", "item-type", "active"]'}

    response = client.put_request(resource_name=f"items/{item_id}", params=params, payload=payload)
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    result = CoupaItemDetails(
        item_id=int(response.get("id", 0)),
        item_name=response.get("name", "No Found"),
        item_number=response.get("item_number"),
        is_active=response.get("active"),
        description=response.get("description"),
        storage_quantity=response.get("storage-quantity"),
        consumption_quantity=response.get("consumption-quantity"),
    )

    return ToolResponse(success=True, message="The item was successfully updated.", content=result)
