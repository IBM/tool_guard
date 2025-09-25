from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class CoupaItemDetails:
    """Represents an a purchase item."""

    item_id: int
    item_name: str
    item_number: Optional[str] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None
    storage_quantity: Optional[int] = None
    consumption_quantity: Optional[int] = None


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_item_by_id(item_id: int) -> ToolResponse[CoupaItemDetails]:
    """
    Retrieves a specific item by its ID from Coupa.

    Args:
        item_id: The Coupa internal ID of the item to retrieve (required).

    Returns:
        details of an item.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failed to retrieve credentials.")

    params = {
        "fields": '["id", "item-number", "name", "description", "active", "storage-quantity", "consumption-quantity"]'
    }

    response = client.get_request(resource_name=f"items/{item_id}", params=params)

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

    return ToolResponse(success=True, message="Folllowing is the item details.", content=result)
