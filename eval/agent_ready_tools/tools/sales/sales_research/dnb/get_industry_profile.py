from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.sales.sales_research.dnb.dnb_schemas import ErrorResponse
from agent_ready_tools.tools.sales.sales_research.dnb.dnb_utils import process_dnb_error
from agent_ready_tools.utils.tool_credentials import DNB_SALES_CONNECTIONS


@dataclass
class IndustryProfileResponse:
    """Dataclass representing the industry profile response from Dnb."""

    profile_name: Optional[str] = None
    industry_overview: Optional[object] = None
    quarterly_industry_update: Optional[object] = None
    previous_quarterly_industry_update: Optional[object] = None
    business_challenges: Optional[object] = None
    trends_and_opportunities: Optional[object] = None
    executive_insight: Optional[object] = None
    # call_preparation_questions: object
    # financial_information: object
    # industry_forecast: object


@tool(expected_credentials=DNB_SALES_CONNECTIONS)
def get_industry_profile(
    duns_number: Optional[int] = None,
    search_term: Optional[str] = None,
    naics_code: Optional[int] = None,
    us_sicv4: Optional[int] = None,
) -> List[IndustryProfileResponse] | ErrorResponse:
    """
    Retrieve a overview report on an industry, market or market sector for a given duns, searchTerm,
    naics or usSICV4.

    At least one of the input params MUST be provided.

    Args:
        duns_number: The duns number to look up, if any, in the search operation
        search_term: The search term to use, if any, in the search operation
        naics_code: The naics code to use, if any, in the search operation
        us_sicv4: The us_sicv4 code to use, if any, in the search operation.

    Returns:
        A list of IndustryProfileResponse objects from the DnB REST API. Each object
        contains:
            - profile_name (str): The name of the industry profile that represents a collection of industries or lines of business.
            - industry_overview (object): High-level details on the primary operation and scope of an industry.
            - quarterly_industry_update (object): The details of the impact on the industry of a challenge, trend, or opportunity covered in the news media or in government statistics issued during the most recent 90 days.
            - previous_quarterly_industry_update (object): The impact on the industry of a challenge, trend, or opportunity covered in the news media or in government statistics issued during the previous quarters.
            - business_challenges (object): The details of the challenges affecting companies in the industry.
            - trends_and_opportunities (object): The details of opportunities available to companies in an industry and business trends affecting companies in the industry.
            - executive_insight (object): The specific actions that senior executives are likely to take to address major strategic issues specific to the industry.
    """
    if not any((duns_number, search_term, naics_code, us_sicv4)):
        raise ValueError(
            "At least one of 'duns_number', 'search_term', 'us_sicv4', or 'naics_code' must be provided."
        )

    # Retrieve the DNB client using the helper function.
    client = get_dnb_client(entitlement=DNBEntitlements.SALES)

    query_parameters = {"productId": "inddet", "versionId": "v1"}

    if duns_number:
        query_parameters["duns"] = str(duns_number)
    elif search_term:
        query_parameters["searchTerm"] = search_term
    elif naics_code:
        query_parameters["naics"] = str(naics_code)
    else:
        query_parameters["usSICV4"] = str(us_sicv4)

    industry_profiles = []

    # Make the GET request with the DNB Client.
    response = client.get_request(
        version="v1",  # The API version.
        category="industryprofile",  # The API category.
        params=query_parameters,  # query parameters
    )

    profiles = response.get("profiles", None)

    # Check if we have an error in the response.
    api_url = "https://plus.dnb.com/v1/industryprofile"
    url_params = query_parameters
    error_response = process_dnb_error(response, api_url, url_params)

    if profiles:
        for profile in profiles:
            industry_profiles.append(
                IndustryProfileResponse(
                    profile_name=profile.get("profileName", ""),
                    industry_overview=profile.get("industryOverview", {}),
                    quarterly_industry_update=profile.get("quarterlyIndustryUpdate", {}),
                    previous_quarterly_industry_update=profile.get(
                        "previousQuarterlyIndustryUpdate", {}
                    ),
                    business_challenges=profile.get("businessChallenges", {}),
                    trends_and_opportunities=profile.get("trendsAndOpportunities", {}),
                    executive_insight=profile.get("executiveInsight", {}),
                    # temp solution to payload issue: remove low priority columns
                    # call_preparation_questions=profile.get("callPreparationQuestions", {}),
                    # financial_information=profile.get("financialInformation", {}),
                    # industry_forecast=profile.get("industryForecast", {}),
                )
            )
            break  # temp solution to payload issue: only store and display the first profile

    # If there is no industry_profiles, then return error_response, else return industry_profiles
    if not industry_profiles or not isinstance(industry_profiles, list):
        return error_response
    else:
        return industry_profiles
