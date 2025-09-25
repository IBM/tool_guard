from typing import Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.sales.sales_research.dnb.dnb_schemas import ErrorResponse
from agent_ready_tools.tools.sales.sales_research.dnb.dnb_utils import process_dnb_error
from agent_ready_tools.utils.tool_credentials import DNB_SALES_CONNECTIONS


@dataclass
class CompanyDetails:
    """Dataclass representing a company response from DnB."""

    primary_name: Optional[str] = None
    duns_number: Optional[str] = None
    address_country: Optional[str] = None
    number_of_employees: Optional[int] = None
    yearly_revenue_value: Optional[float] = None
    yearly_revenue_currency: Optional[str] = None
    industry_name: Optional[str] = None


@tool(expected_credentials=DNB_SALES_CONNECTIONS)
def get_industry_peers_by_name(industry_code: str) -> List[CompanyDetails] | ErrorResponse:
    """
    Takes a usSicV4 (Industry Code) for a company and returns a list of companies with the same
    usSicV4 (Industry Code)

    Args:
        industry_code: The industry code for a company retrieved by search_company_by_typeahead

    Returns:
        The list of Companies object which have the same `usSicV4` code from the DnB
        Search Criteria REST API. Each object contains:
            - primary_name (str): The single name by which the organization is primarily known / identified.
            - duns_number (str): The D-U-N-S Number is D&B's identification number, which provides unique identification of this organization
            - industry_name (str): The business activity based on the scheme used for the industry code
            - address_country (str): The country or region for this address of the organization.
            - number_of_employees (int): The number of individuals engaged by a business to perform its various purposes and includes the Consolidated count
            - yearly_revenue_value (str): The annual sales or revenue of the company.
            - yearly_revenue_currency (str): The three-letter currency code, identifying the type of money in which this amount is expressed (e.g., USD, CAD, GBP, EUR).
    """
    search_criteria: Dict[str, object] = {
        "usSicV4": [industry_code],
    }
    client = get_dnb_client(entitlement=DNBEntitlements.SALES)
    response = client.post_request(
        version="v1",
        category="search",
        endpoint="criteria",
        data=search_criteria,
    )

    search_candidates = response.get("searchCandidates", None)
    # Check if we have an error in the response.
    api_url = "https://plus.dnb.com/v1/search/criteria"
    url_params = search_criteria
    error_response = process_dnb_error(response, api_url, url_params)

    company_list: List[CompanyDetails] = []
    if search_candidates:
        for candidate in search_candidates:
            organization = candidate.get("organization", None)
            primary_address = organization.get("primaryAddress", None)

            primary_address_country = primary_address.get("addressCountry", None)

            primary_industry_code = organization.get("primaryIndustryCodes", [{}])[0]

            company_financials = (
                organization.get("financials", [{}])[0].get("yearlyRevenue", [{}])[0]
                if organization.get("financials")
                else {}
            )

            company_list.append(
                CompanyDetails(
                    duns_number=organization.get("duns", None),
                    primary_name=organization.get("primaryName", None),
                    industry_name=primary_industry_code.get("usSicV4Description", None),
                    address_country=primary_address_country.get("name", None),
                    number_of_employees=next(
                        (
                            item.get("value")
                            for item in organization.get("numberOfEmployees", [])
                            if item.get("informationScopeDescription") == "Consolidated"
                        ),
                        None,  # Default value if no "Consolidated" entry is found
                    ),
                    yearly_revenue_value=company_financials.get("value", None),
                    yearly_revenue_currency=company_financials.get("currency", None),
                )
            )
    # If there is no company_list, then return error_response, else return company_list
    if not company_list or not isinstance(company_list, list):
        return error_response
    else:
        return company_list
