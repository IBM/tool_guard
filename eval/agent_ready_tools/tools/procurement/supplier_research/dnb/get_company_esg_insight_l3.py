from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import DNB_PROCUREMENT_CONNECTIONS


@dataclass
class ESGInsight:
    """Represents a financial strength of a company."""

    duns_number: str
    esg_score: Optional[int] = None
    esg_ranking: Optional[str] = None
    environmental_score: Optional[int] = None
    social_score: Optional[int] = None
    governance_score: Optional[int] = None
    health_safety_score: Optional[str] = None
    diversity_inclusion_score: Optional[str] = None
    human_rights_abuses_score: Optional[str] = None
    labor_relations_score: Optional[str] = None


@tool(expected_credentials=DNB_PROCUREMENT_CONNECTIONS)
def dnb_get_company_esg_insight_l3(duns_number: str) -> ToolResponse[ESGInsight]:
    """
    Returns the company's ESG ranking and insight.

    Args:
        duns_number: The company's duns number.

    Returns:
        The level 1 esg insight.
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

    if org is None or "esgRanking" not in org:
        return ToolResponse(
            success=False, message="The information is not available for this company"
        )

    result = ESGInsight(duns_number=org["duns"])

    result.esg_score = org["esgRanking"].get("score")
    result.esg_ranking = org["esgRanking"].get("dataDepth", {}).get("indicator")
    result.environmental_score = org["esgRanking"].get("environmentalRanking", {}).get("score")
    result.social_score = org["esgRanking"].get("socialRanking", {}).get("score")
    result.governance_score = org["esgRanking"].get("governanceRanking", {}).get("score")
    result.health_safety_score = (
        org["esgRanking"]
        .get("socialRanking", {})
        .get("humanCapitalTopics", {})
        .get("healthSafetyScore")
    )
    result.diversity_inclusion_score = (
        org["esgRanking"]
        .get("socialRanking", {})
        .get("humanCapitalTopics", {})
        .get("diversityInclusionScore")
    )
    result.human_rights_abuses_score = (
        org["esgRanking"]
        .get("socialRanking", {})
        .get("humanCapitalTopics", {})
        .get("humanRightsAbusesScore")
    )
    result.labor_relations_score = (
        org["esgRanking"]
        .get("socialRanking", {})
        .get("humanCapitalTopics", {})
        .get("laborRelationsScore")
    )
    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
