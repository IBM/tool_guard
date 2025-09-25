from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.purchase_dataclasses import (
    OracleFusionSpecialHandlingTypesHeader,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_get_special_handling_types(
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[List[OracleFusionSpecialHandlingTypesHeader]]:
    """
    Gets all the special handling types from Oracle Fusion.

    Args:
        limit: The maximum number of records returned per page.
        skip: The number of records to skip for pagination.

    Returns:
        A list of special handling types.
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params: Dict[str, Any] = {"limit": limit, "offset": skip}

    response = client.get_request(resource_name=f"specialHandlingTypes", params=params)

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    if "items" not in response or len(response["items"]) == 0:
        return ToolResponse(success=False, message="No special handling types returned.")

    special_handling_types = []

    for special_handling_type in response["items"]:
        special_handling_types.append(
            OracleFusionSpecialHandlingTypesHeader(
                special_handling_type=special_handling_type.get("SpecialHandlingType", ""),
                special_handling_type_code=special_handling_type.get("SpecialHandlingTypeCode", ""),
            )
        )

    return ToolResponse(
        success=True,
        message="Retrieved the special handling types from Oracle Fusion successfully.",
        content=special_handling_types,
    )
