from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import DNB_PROCUREMENT_CONNECTIONS


@dataclass
class MatchedCompany:
    """Represents a single company."""

    duns_number: str
    primary_name: str


@tool(expected_credentials=DNB_PROCUREMENT_CONNECTIONS)
def dnb_search_company_by_name(
    search_query: str, country: str = "US"
) -> ToolResponse[list[MatchedCompany]]:
    """
    Searches for a company using a search term and returns the duns number.

    Args:
        search_query: The search term.
        country: The country ISO code.

    Returns:
        The matched companies.
    """
    try:
        client = get_dnb_client(entitlement=DNBEntitlements.PROCUREMENT)
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {"name": search_query, "countryISOAlpha2Code": country}
    response = client.get_request("v1", "match", "cleanseMatch", params=params)
    if "error" in response and "errorMessage" in response["error"]:
        return ToolResponse(success=False, message=response["error"]["errorMessage"])

    if "matchCandidates" not in response:
        return ToolResponse(success=False, message="No company was matched with your query")

    matched_candidates: list[MatchedCompany] = []

    for candidate in response["matchCandidates"]:
        if candidate["matchQualityInformation"]["nameMatchScore"] <= 0.75:
            continue

        org = candidate["organization"]
        matched_candidates.append(
            MatchedCompany(duns_number=org["duns"], primary_name=org["primaryName"])
        )
    if len(matched_candidates) > 0:
        return ToolResponse(
            success=True, message="The data was successfully retrieved", content=matched_candidates
        )
    else:
        return ToolResponse(
            success=False, message="No company was matched with your query", content=[]
        )
