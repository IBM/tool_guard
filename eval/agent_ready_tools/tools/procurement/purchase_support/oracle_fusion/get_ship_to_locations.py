from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.purchase_dataclasses import (
    OracleFusionShipToLocationHeader,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_get_ship_to_locations(
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[List[OracleFusionShipToLocationHeader]]:
    """
    Gets all the ship to locations (common set) from Oracle Fusion.

    Args:
        limit: The maximum number of records returned per page.
        skip: The number of records to skip for pagination.

    Returns:
        A list of ship to locations.
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params: Dict[str, Any] = {"limit": limit, "offset": skip, "q": "SetName='Common Set'"}

    response = client.get_request(resource_name=f"b2bShipToLocationsLOV", params=params)

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    if "items" not in response or len(response["items"]) == 0:
        return ToolResponse(success=False, message="No ship-to locations returned.")

    ship_to_locations = []

    for ship_to_location in response["items"]:
        ship_to_locations.append(
            OracleFusionShipToLocationHeader(
                location_id=ship_to_location.get("LocationId", -1),
                location_name=ship_to_location.get("LocationName", ""),
                address=ship_to_location.get("Address", ""),
            )
        )

    return ToolResponse(
        success=True,
        message="Retrieved the ship to locations from Oracle Fusion successfully.",
        content=ship_to_locations,
    )
