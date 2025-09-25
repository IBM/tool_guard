from typing import Any, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class CoupaCommodities:
    """Represents commodities in coupa."""

    name: str
    parent_name: str
    is_active: bool


@dataclass
class CoupaCommoditiesResponse:
    """Represents the result of get_commodites in coupa."""

    commodities: List[CoupaCommodities]


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_commodities(
    commodity_name: Optional[str] = None,
    limit: Optional[int] = 20,
    offset: Optional[int] = 0,
) -> ToolResponse[CoupaCommoditiesResponse]:
    """
    Get's all the available commodities present in Coupa.

    Args:
        commodity_name: The name of the commodity.
        limit: Optional, the count of purchase orders to return - default 20.
        offset: Optional, the number of entries to offset by for pagination - default 0.

    Returns:
        List of commodities.
    """

    params: dict[str, Any] = {
        key: value
        for key, value in {
            "name[contains]": commodity_name,
            "limit": limit,
            "offset": offset,
        }.items()
        if value
    }

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failed to retrieve credentials.")

    response = client.get_request_list(resource_name="commodities", params=params)

    if len(response) == 1 and "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    commodities_list: List[CoupaCommodities] = []

    for item in response:
        commodities_list.append(
            CoupaCommodities(
                name=item.get("name", ""),
                parent_name=item.get("parent", {}).get("name", ""),
                is_active=item.get("active", ""),
            )
        )
    return ToolResponse(
        success=True,
        message="Here is the list of commodities.",
        content=CoupaCommoditiesResponse(commodities=commodities_list),
    )
