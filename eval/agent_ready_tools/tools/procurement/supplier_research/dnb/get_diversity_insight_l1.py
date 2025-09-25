from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import DNB_PROCUREMENT_CONNECTIONS


@dataclass
class DiversityInsight:
    """Represents a financial strength of a company."""

    duns_number: str
    is_eight_a_certification: Optional[bool] = None
    is_minority_owned: Optional[bool] = None
    is_women_owned: Optional[bool] = None
    is_veteran_owned: Optional[bool] = None
    is_vietnam_veteran_owned: Optional[bool] = None
    ethnicity_type: Optional[str] = None


@tool(expected_credentials=DNB_PROCUREMENT_CONNECTIONS)
def dnb_get_diversity_insight_l1(duns_number: str) -> ToolResponse[DiversityInsight]:
    """
    Returns the company's Diversity Insights.

    Args:
        duns_number: The company's duns number.

    Returns:
        The level 1 Diversity Insights.
    """
    try:
        client = get_dnb_client(entitlement=DNBEntitlements.PROCUREMENT)
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {"blockIDs": "diversityinsight_L1_v1"}
    response = client.get_request("v1", "data", "duns/" + duns_number, params=params)
    if "error" in response and "errorMessage" in response["error"]:
        return ToolResponse(success=False, message=response["error"]["errorMessage"])

    # Build the CompanyInfoResponse object for return
    org = response.get("organization")

    if org is None or "socioEconomicInformation" not in org:
        return ToolResponse(
            success=False, message="The information is not available for this company"
        )

    result = DiversityInsight(duns_number=org["duns"])

    result.duns_number = org.get("duns", "")
    result.is_women_owned = org.get("socioEconomicInformation", {}).get("isWomanOwned")
    result.is_minority_owned = org.get("socioEconomicInformation", {}).get("isMinorityOwned")
    result.is_veteran_owned = org.get("socioEconomicInformation", {}).get("isVeteranOwned")
    result.is_eight_a_certification = org.get("socioEconomicInformation", {}).get(
        "is8ACertifiedBusiness"
    )
    result.is_vietnam_veteran_owned = org.get("socioEconomicInformation", {}).get(
        "isVietnamVeteranOwned"
    )
    result.ethnicity_type = (
        org.get("socioEconomicInformation", {})
        .get("ownershipPrimaryEthnicityType", {})
        .get("description", "")
    )

    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
