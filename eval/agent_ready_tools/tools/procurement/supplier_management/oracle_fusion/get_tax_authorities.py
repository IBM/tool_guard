from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.supplier_dataclasses import (
    OracleFusionTaxAuthorities,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_get_tax_authorities(
    tax_authority_name: Optional[str] = None,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
) -> ToolResponse[List[OracleFusionTaxAuthorities]]:
    """
    Get all tax authorities from Oracle Fusion.

    Args:
        tax_authority_name: The name of the tax authority.
        limit: The maximum number of tax authorities to return.
        offset: The number of tax authorities to skip for pagination.

    Returns:
        A list of tax autorities
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params: Dict[str, Any] = {"limit": limit, "offset": offset}

    if tax_authority_name:
        params["q"] = f"PartyName='{tax_authority_name}'"

    response = client.get_request(
        resource_name="taxAuthorityProfiles",
        params=params,
    )

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    if "items" not in response or len(response["items"]) == 0:
        return ToolResponse(success=False, message="No tax authorities returned")

    tax_authorities = []
    for tax in response["items"]:
        tax_authorities.append(
            OracleFusionTaxAuthorities(
                tax_authority_id=tax["PartyTaxProfileId"],
                tax_authority_name=tax["PartyName"],
            )
        )

    return ToolResponse(
        success=True,
        message="Retrieved a list of tax authorities from Oracle Fusion successfully",
        content=tax_authorities,
    )
