from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class RecruitingOrganizationData:
    """Represents the details of the recruiting organization data from Oracle HCM."""

    organization_id: int
    organization_name: str
    organization_type: str


@dataclass
class GetRecruitingOrganizationsResponse:
    """The response containing the list of recruiting organization details from Oracle HCM."""

    recruiting_organizations: List[RecruitingOrganizationData]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_recruiting_organizations(
    limit: Optional[int] = 20,
    offset: Optional[int] = 0,
) -> GetRecruitingOrganizationsResponse:
    """
    Gets a list of recruiting organization details from Oracle HCM.

    Args:
        limit: The maximum number of records to return. Default is 20.
        offset: The starting point in the record set. Default is 0.

    Returns:
        The response containing the list of recruiting organization details.
    """

    client = get_oracle_hcm_client()
    params = {"limit": limit, "offset": offset}
    response = client.get_request(entity="recruitingOrganizationsLOV", params=params)
    recruiting_organization_list = [
        RecruitingOrganizationData(
            organization_id=organizations.get("OrganizationId", None),
            organization_name=organizations.get("Name", ""),
            organization_type=organizations.get("Orgtype", ""),
        )
        for organizations in response.get("items", [])
    ]

    return GetRecruitingOrganizationsResponse(recruiting_organizations=recruiting_organization_list)
