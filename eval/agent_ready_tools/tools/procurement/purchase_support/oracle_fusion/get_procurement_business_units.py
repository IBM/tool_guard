from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.purchase_dataclasses import (
    OracleFusionProcurementBUHeader,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_get_procurement_business_units(
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[List[OracleFusionProcurementBUHeader]]:
    """
    Gets all the procurement business units from Oracle Fusion.

    Args:
        limit: The maximum number of records returned per page.
        skip: The number of records to skip for pagination.

    Returns:
        A list of procurement business units.
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params: Dict[str, Any] = {"limit": limit, "offset": skip}

    response = client.get_request(resource_name=f"procurementBusinessUnitsLOV", params=params)

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    if "items" not in response or len(response["items"]) == 0:
        return ToolResponse(success=False, message="No procurement business units returned.")

    procurement_business_units = []

    for procurement_business_unit in response["items"]:
        procurement_business_units.append(
            OracleFusionProcurementBUHeader(
                procurement_business_unit_id=procurement_business_unit.get("ProcurementBUId", -1),
                procurement_business_unit=procurement_business_unit.get("ProcurementBU", ""),
            )
        )

    return ToolResponse(
        success=True,
        message="Retrieved the procurement business units from Oracle Fusion successfully.",
        content=procurement_business_units,
    )
