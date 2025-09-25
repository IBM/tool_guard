from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import DNB_PROCUREMENT_CONNECTIONS


@dataclass
class GHGData:
    """Offer insights into a company's direct and indirect Green House Gas Emissions."""

    duns_number: str
    climate_score: Optional[int] = None
    emissions_score: Optional[int] = None
    emission_scope1_volume: Optional[float] = None
    emission_scope2_volume: Optional[float] = None
    emission_scope3_volume: Optional[float] = None
    emission_offset_volume: Optional[float] = None
    emission_offset_scope: Optional[str] = ""
    emission_neutral_year: Optional[str] = ""
    emission_neutral_scopes: Optional[str] = ""
    emission_neutral_type: Optional[str] = ""


@tool(expected_credentials=DNB_PROCUREMENT_CONNECTIONS)
def dnb_get_company_ghg_insight_l3(duns_number: str) -> ToolResponse[GHGData]:
    """
    Returns the company's GHG data.

    Args:
        duns_number: The company's duns number.

    Returns:
        The GHG data.
    """
    try:
        client = get_dnb_client(entitlement=DNBEntitlements.PROCUREMENT)
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {"blockIDs": "esginsight_L3_v1"}
    response = client.get_request("v1", "data", "duns/" + duns_number, params=params)
    if "error" in response and "errorMessage" in response["error"]:
        return ToolResponse(success=False, message=response["error"]["errorMessage"])

    org = response.get("organization")

    if org is None or "esgRanking" not in org or "environmentalRanking" not in org["esgRanking"]:
        return ToolResponse(
            success=False, message="The information is not available for this company"
        )

    result = GHGData(duns_number=org["duns"])

    env_ranking = org.get("esgRanking", {}).get("environmentalRanking")

    result.climate_score = env_ranking.get("emissionsClimateTopics", {}).get("climateRiskScore")
    result.emissions_score = env_ranking.get("emissionsClimateTopics", {}).get("ghgEmissionsScore")

    result.emission_scope1_volume = env_ranking.get("ghgEmissionScope1", {}).get("emissionVolume")
    result.emission_scope2_volume = env_ranking.get("ghgEmissionScope2", {}).get("emissionVolume")
    result.emission_scope3_volume = env_ranking.get("ghgEmissionScope3", {}).get("emissionVolume")

    result.emission_offset_volume = env_ranking.get("emissionOffset", {}).get("offsetVolume")
    result.emission_offset_scope = env_ranking.get("emissionOffset", {}).get("emissionScopes")

    result.emission_neutral_year = env_ranking.get("emissionNeutralPlan", {}).get(
        "emissionNeutralYear"
    )
    result.emission_neutral_scopes = env_ranking.get("emissionNeutralPlan", {}).get(
        "emissionNeutralScopes"
    )
    result.emission_neutral_type = env_ranking.get("emissionNeutralPlan", {}).get(
        "emissionNeutralType"
    )

    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
