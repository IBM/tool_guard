from typing import Any, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import DNB_PROCUREMENT_CONNECTIONS


@dataclass
class HierarchiesAndConnections:
    """Represents the Hierarchies and Connetions within a company."""

    duns_number: str
    family_tree_roles: Optional[List[Any]] = None
    family_tree_member_count: Optional[int] = None
    global_ultimate: Optional[str] = ""
    domestic_ultimate: Optional[str] = ""
    hierarchy_level: Optional[int] = None
    branches: Optional[List[Any]] = None
    branches_count: Optional[int] = None


@tool(expected_credentials=DNB_PROCUREMENT_CONNECTIONS)
def dnb_get_hierarchies_and_connections_l1(
    duns_number: str,
) -> ToolResponse[HierarchiesAndConnections]:
    """
    Returns the company's Hierarchies and Connections.

    Args:
        duns_number: The company's duns number.

    Returns:
        The level 1 Hierarchies and Connections.
    """
    try:
        client = get_dnb_client(entitlement=DNBEntitlements.PROCUREMENT)
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {"blockIDs": "hierarchyconnections_L1_v1"}
    response = client.get_request("v1", "data", "duns/" + duns_number, params=params)
    if "error" in response and "errorMessage" in response["error"]:
        return ToolResponse(success=False, message=response["error"]["errorMessage"])

    # Build the CompanyInfoResponse object for return
    org = response.get("organization")

    if org is None or "corporateLinkage" not in org:
        return ToolResponse(
            success=False, message="The information is not available for this company"
        )

    result = HierarchiesAndConnections(duns_number=org["duns"])

    result.family_tree_roles = org["corporateLinkage"].get("familytreeRolesPlayed")
    result.global_ultimate = (
        org["corporateLinkage"].get("globalUltimate", {}).get("primaryName", "")
    )
    result.domestic_ultimate = (
        org["corporateLinkage"].get("domesticUltimate", {}).get("primaryName", "")
    )
    result.family_tree_member_count = org["corporateLinkage"].get(
        "globalUltimateFamilyTreeMembersCount"
    )
    result.hierarchy_level = org["corporateLinkage"].get("hierarchyLevel")
    result.branches_count = org["corporateLinkage"].get("branchesCount")
    result.branches_count = org["corporateLinkage"].get("branches")

    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
