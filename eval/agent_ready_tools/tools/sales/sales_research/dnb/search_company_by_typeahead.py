from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.sales.sales_research.dnb.dnb_schemas import ErrorResponse
from agent_ready_tools.tools.sales.sales_research.dnb.dnb_utils import process_dnb_error
from agent_ready_tools.utils.tool_credentials import DNB_SALES_CONNECTIONS


@dataclass
class CompanyMatched:
    """Represents a single company matched with search request."""

    primary_name: Optional[str] = None
    duns_number: Optional[str] = None
    address_country: Optional[str] = None
    address_region: Optional[str] = None
    yearly_revenue_value: Optional[float] = None
    revenue_currency: Optional[str] = None
    industry_code: Optional[str] = None
    industry_name: Optional[str] = None


@tool(expected_credentials=DNB_SALES_CONNECTIONS)
def search_company_by_typeahead(
    search_query: str, country: str = "US"
) -> list[CompanyMatched] | ErrorResponse:
    """
    Searches for a company using their primary or tradestyle name and returns the top company
    matching that name.

    This includes full company name, duns number, address information, yearly
    revenue, currency, IndustryCode (usSicV4) and IndustryName (usSicV4Description).

    Args:
        search_query: The name of the compnay
        country: The country code is optional and US in included as default

    Returns:
        The list of CompanyResponses objects from the DnB REST API. Each object
        contains:
            - primary_name (Optional[str]): Single name by which the organization is primarily known or identified.
            - duns_number (Optional[str]): unique identification of a subject organization
            - address_country (Optional[str]): The two-letter country code where the business is located
            - address_region (Optional[str]): The name of the geographical area for this address of the organization
            - yearly_revenue_value (Optional[float]): The annual sales or revenue of the company.
            - revenue_currency (Optional[str]): The three-letter currency code, defined in the ISO 4217 scheme
            - industry_code (Optional[str]): An alphanumeric value assigned to an organization categorizing the business activities performed at its location
            - industry_name (Optional[str]): The business activity based on the scheme used for the industry code
    """

    client = get_dnb_client(entitlement=DNBEntitlements.SALES)
    params = {"searchTerm": search_query, "countryISOAlpha2Code": country}
    response = client.get_request("v1", "search", "typeahead", params=params)

    search_candidates: list[CompanyMatched] = []

    # Check if we have an error in the response.
    api_url = "https://plus.dnb.com/v1/search/typeahead"
    url_params = params
    error_response = process_dnb_error(response, api_url, url_params)

    # If we dont return any searchCandidates, then return the error_response
    if "searchCandidates" not in response:
        return error_response

    for candidate in response["searchCandidates"]:
        if candidate["displaySequence"] > 1:
            continue

        company_info = candidate.get("organization", None)
        company_info_address_country = company_info.get("primaryAddress", None).get(
            "addressCountry", None
        )
        company_info_address_region = company_info.get("primaryAddress", None).get(
            "addressRegion", None
        )
        company_info_financial_revenue = (
            company_info.get("financials", [{}])[0].get("yearlyRevenue", [{}])[0]
            if company_info.get("financials")
            else {}
        )
        company_info_industry_codes = company_info.get("primaryIndustryCodes", [{}])[0]

        search_candidates.append(
            CompanyMatched(
                primary_name=company_info.get("primaryName", None),
                duns_number=company_info.get("duns", None),
                address_country=company_info_address_country.get("isoAlpha2Code", None),
                address_region=company_info_address_region.get("name", None),
                yearly_revenue_value=company_info_financial_revenue.get("value", None),
                revenue_currency=company_info_financial_revenue.get("currency", None),
                industry_code=company_info_industry_codes.get("usSicV4", None),
                industry_name=company_info_industry_codes.get("usSicV4Description", None),
            )
        )

    # If there is no search_candidates, then return error_response, else return search_candidates
    if not search_candidates or not isinstance(search_candidates, list):
        return error_response
    else:
        return search_candidates
