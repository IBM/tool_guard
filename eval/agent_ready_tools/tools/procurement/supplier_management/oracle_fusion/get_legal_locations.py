from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.supplier_dataclasses import (
    OracleFusionLegalLocations,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_get_legal_locations(
    tax_registration_id: str,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
) -> ToolResponse[List[OracleFusionLegalLocations]]:
    """
    Get all legal locations from Oracle Fusion.

    Args:
        tax_registration_id: The id of the supplier tax registration, returned by the oracle_fusion_get_supplier_tax_registrations tool.
        limit: The maximum number of legal locations to return.
        offset: The number of legal locations to skip for pagination.

    Returns:
        A list of legal locations
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {"limit": limit, "offset": offset}

    response = client.get_request(
        resource_name=f"taxRegistrations/{tax_registration_id}/lov/legalLocations",
        params=params,
    )

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    if "items" not in response or len(response["items"]) == 0:
        return ToolResponse(success=False, message="No legal locations returned")

    legal_locations = []
    for location in response["items"]:
        legal_locations.append(
            OracleFusionLegalLocations(
                location_id=location["LocationId"],
                address=location["FormattedAddress"],
            )
        )

    return ToolResponse(
        success=True,
        message="Retrieved a list of legal locations from Oracle Fusion successfully",
        content=legal_locations,
    )
