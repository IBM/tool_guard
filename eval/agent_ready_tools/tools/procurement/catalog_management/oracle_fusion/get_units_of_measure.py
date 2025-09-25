from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.catalog_dataclasses import (
    OracleFusionUOM,
)
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_get_units_of_measure(
    limit: Optional[int] = None, offset: Optional[int] = None
) -> ToolResponse[List[OracleFusionUOM]]:
    """
    Retrieves a list of available Units of Measure (UoM) from Oracle Fusion.

    Args:
        limit: The maximum number of records to return.
        offset: The number of records to skip for pagination.

    Returns:
        A ToolResponse object containing the list of UoMs or an error message.
    """
    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError) as e:
        return ToolResponse(success=False, message=f"Failure to retrieve credentials: {e}")

    params: Dict[str, Any] = {}
    if limit:
        params["limit"] = limit
    if offset:
        params["offset"] = offset

    response = client.get_request(
        resource_name="unitsOfMeasure",
        params=params,
    )

    if "errors" in response or "error" in response:
        error_message = response.get("errors", response.get("error", "Unknown API error"))
        return ToolResponse(success=False, message=str(error_message))

    uom_list = []
    for item in response.get("items", []):
        uom_code = item.get("UOMCode")

        if uom_code:
            uom_list.append(
                OracleFusionUOM(
                    uom_code=uom_code,
                    description=item.get("Description"),
                    uom_class_name=item.get("UOMClassName"),
                    base_unit_flag=item.get("BaseUnitFlag"),
                )
            )

    return ToolResponse(
        success=True,
        message=f"Successfully retrieved {len(uom_list)} Units of Measure.",
        content=uom_list,
    )
