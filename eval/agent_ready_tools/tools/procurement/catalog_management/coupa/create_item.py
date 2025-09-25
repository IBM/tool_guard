from typing import Optional  # Use typing for Optional and Dict

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_create_item(
    name: str,
    uom_code: str = "EA",
    item_number: Optional[str] = None,
    description: Optional[str] = None,
    active: bool = True,
    manufacturer_name: Optional[str] = None,
    manufacturer_part_number: Optional[str] = None,
    item_type: str = "Item",
) -> ToolResponse[int]:
    """
    Adds a new item to Coupa by making a POST request.

    Args:
        name: Name of the item to add (required).
        uom_code: Unit Of Measure code for the item (e.g., "EA", "BOX") (required).
        item_number: Unique item number/SKU (optional, but highly recommended, default=None).
        description: Description of the item (optional, default=None).
        active: Whether the item is active (optional, default=True).
        manufacturer_name: Name of the manufacturer (optional, default=None).
        manufacturer_part_number: Manufacturer's part number (optional, default=None).
        item_type: Type of item, usually "Item" (optional, default="Item").

    Returns:
        The item_id.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failed to retrieve credentials.")

    payload = {
        "name": name,
        "active": active,
        "item-type": item_type,
        "uom": {"code": uom_code},
    }

    if item_number is not None:
        payload["item-number"] = item_number
    if description is not None:
        payload["description"] = description
    if manufacturer_name is not None:
        payload["manufacturer-name"] = manufacturer_name
    if manufacturer_part_number is not None:
        payload["manufacturer-part-number"] = manufacturer_part_number

    response = client.post_request(resource_name="items", payload=payload)
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message=f"The item was successfully created with item_id {response["id"]}",
        content=response["id"],
    )
