from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.catalog_management.coupa.get_item_by_id import (
    CoupaItemDetails,
)
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class CoupaSearchItemResponse:
    """Represents a list of item details to be used as response."""

    total_count: int
    found_items: list[CoupaItemDetails]


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_search_item_by_name(search_term: str) -> ToolResponse[CoupaSearchItemResponse]:
    """
    search for an item in coupa using provided search term and returns suppliers of that item.

    Args:
        search_term: The search term.

    Returns:
        The best match results.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failed to retrieve credentials.")

    params = {
        "name[contains]": search_term,
        "fields": '["id", "item-number", "name", "description", "active", "storage-quantity", "consumption-quantity"]',
    }

    response = client.get_request_list(resource_name="items", params=params)
    if len(response) == 1 and "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    if len(response) == 0:
        return ToolResponse(
            success=True,
            message="There are no items found in the catalog. Please provide another search term.",
        )

    result = CoupaSearchItemResponse(
        total_count=len(response),
        found_items=[
            CoupaItemDetails(
                item_id=int(r.get("id", 0)),
                item_name=r.get("name", ""),
                item_number=r.get("item_number", None),
                is_active=r.get("active", None),
                description=r.get("description", None),
                storage_quantity=r.get("storage-quantity", None),
                consumption_quantity=r.get("consumption-quantity", None),
            )
            for r in response
        ],
    )

    return ToolResponse(
        success=True,
        message="Following is the list of items based on your search term",
        content=result,
    )
