from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import DNB_PROCUREMENT_CONNECTIONS


@dataclass
class BeneficialOwnershipInsight:
    """Represents beneficial ownership information of a company."""

    duns_number: str
    beneficial_owners_count: Optional[str] = None
    relationships_count: Optional[str] = None
    maximum_degree_of_separation: Optional[int] = None
    total_allocated_ownership_percentage: Optional[int] = None
    organizations_count: Optional[str] = None
    individuals_count: Optional[float] = None
    corporate_beneficiaries_count: Optional[float] = None
    state_owned_organizations_count: Optional[float] = None
    government_organizations_count: Optional[float] = None
    publicly_trading_organizations_count: Optional[float] = None
    privately_held_organizations_count: Optional[int] = None
    psc_unique_type_count: Optional[str] = None
    country_wise_psc_summary: Optional[str] = None
    country_unknown_psc_count: Optional[str] = None


@tool(expected_credentials=DNB_PROCUREMENT_CONNECTIONS)
def dnb_get_beneficial_ownership_insight_l2(
    duns_number: str,
) -> ToolResponse[BeneficialOwnershipInsight]:
    """
    Returns the company beneficial ownership insight.

    Args:
        duns_number: The company's duns number.

    Returns:
        The level 2 of beneficial ownership insight.
    """

    try:
        client = get_dnb_client(entitlement=DNBEntitlements.PROCUREMENT)
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {
        "ownershipType": "BENF_OWRP",
        "productId": "cmpbol",
        "versionId": "v1",
        "duns": duns_number,
    }

    response = client.get_request("v1", "beneficialowner", params=params)
    if "error" in response and "errorMessage" in response["error"]:
        return ToolResponse(success=False, message=response["error"]["errorMessage"])

    org = response.get("organization")

    if org is None or "beneficialOwnershipSummary" not in org:
        return ToolResponse(
            success=False, message="The information is not available for this company"
        )

    result = BeneficialOwnershipInsight(duns_number=org["duns"])
    benf_summary = org["beneficialOwnershipSummary"]
    result.beneficial_owners_count = benf_summary.get("beneficialOwnersCount")
    result.relationships_count = benf_summary.get("relationshipsCount")
    result.maximum_degree_of_separation = benf_summary.get("maximumDegreeOfSeparation")
    result.total_allocated_ownership_percentage = benf_summary.get(
        "totalAllocatedOwnershipPercentage"
    )
    result.organizations_count = benf_summary.get("organizationsCount")
    result.individuals_count = benf_summary.get("individualsCount")
    result.corporate_beneficiaries_count = benf_summary.get("corporateBeneficiariesCount")
    result.state_owned_organizations_count = benf_summary.get("stateOwnedOrganizationsCount")
    result.government_organizations_count = benf_summary.get("govermentOrganiztionsCount")
    result.publicly_trading_organizations_count = benf_summary.get(
        "publiclyTradingOrganizationsCount"
    )
    result.privately_held_organizations_count = benf_summary.get("privatelyHeldOrganizationsCount")
    result.psc_unique_type_count = benf_summary.get("pscUniqueTypeCount")

    result.country_wise_psc_summary = benf_summary.get("countryWisePSCSummary")
    result.country_unknown_psc_count = benf_summary.get("countryUnknownPSCCount")

    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
