from enum import StrEnum
from typing import Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import BaseModel, ConfigDict, Field

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.sales.sales_research.dnb.dnb_schemas import ErrorResponse
from agent_ready_tools.tools.sales.sales_research.dnb.dnb_utils import process_dnb_error
from agent_ready_tools.utils.tool_credentials import DNB_SALES_CONNECTIONS


class EnrichedMatchedCompany(BaseModel):
    """Represents a single company matched with search request."""

    model_config = ConfigDict(extra="ignore")  # Ignore extra fields

    primary_name: Optional[str] = Field(alias="primaryName", default=None)
    duns_number: Optional[str] = Field(alias="duns", default=None)
    number_of_employees: Optional[int] = Field(alias="employeeCount", default=None)
    address_region: Optional[str] = Field(alias="addressRegion", default=None)
    address_country: Optional[str] = Field(alias="addressCountry", default=None)
    yearly_revenue_value: Optional[float] = Field(alias="revenue", default=None)
    industry_name: Optional[str] = Field(alias="industryDescription", default=None)

    @classmethod
    def from_api_response(cls, data: Dict) -> "EnrichedMatchedCompany":
        """
        Validate/mutate response data to have all necessary info at top level and instantiate
        EnrichedMatchedCompany.

        Args:
            data: keys and values to initialize object with.

        Returns:
            data with necessary info at top level.
        """
        if "employeeCount" in data:
            # dict in good condition, return
            return cls(**data)
        if "numberOfEmployees" in data:
            number_of_employees = data.pop("numberOfEmployees")
            data["employeeCount"] = number_of_employees[0]["value"]
        else:
            data["employeeCount"] = 0
        financials = data.pop("financials")
        yearly_revenue = financials[0].pop("yearlyRevenue")
        data["revenue"] = yearly_revenue[0]["value"]
        primary_industry_code = data.pop("primaryIndustryCodes")
        data["industryDescription"] = primary_industry_code[0]["usSicV4Description"]
        address_info = data.pop("primaryAddress")
        address_country = address_info.pop("addressCountry")
        data["addressCountry"] = address_country["isoAlpha2Code"]
        if "addressRegion" in address_info:
            address_region = address_info.pop("addressRegion")
            data["addressRegion"] = address_region["name"]
        else:
            data["addressRegion"] = ""
        return cls(**data)


class CorpTypes(StrEnum):
    """List of corporation types, for use in DnB queries."""

    INC = "inc"
    CORP = "co"
    LTD = "ltd"
    LP = "lp"
    PTE = "pte"
    GMBH = "gmbh"
    BV = "bv"
    SA = "sa"
    OOO = "ooo"


@tool(expected_credentials=DNB_SALES_CONNECTIONS)
def search_company_by_criteria(
    ussicv4_code: Optional[str] = None,
    address_region: Optional[str] = None,
    address_country: str = "US",
    employee_min_count: int = 1,
    employee_max_count: int = 999999,
    revenue_min_quantity: int = 1,
    revenue_max_quantity: int = 100000000000000,
) -> List[EnrichedMatchedCompany] | ErrorResponse:
    """
    Search for companies using one or more of the filters: industry, location, employee count, and
    revenue.

    Args:
        ussicv4_code: US SIC V4 code string of company industry.
        address_region: The region or city of the company.
        address_country: The country ISO code.
        employee_min_count: The minimum number of employees a company you are interested in should
            have.
        employee_max_count: The maximum number of employees a company you are interested in should
            have.
        revenue_min_quantity: The minimum revenue a company you are interested in should have.
        revenue_max_quantity: The maximum revenue a company you are interested in should have.

    Returns:
        A list of matched company objects. Each object includes:
            - primary_name (str): Single name by which the organization is primarily known or identified.
            - duns_number (str):  unique identification of a subject organization,
            - number_of_employees (int): the number of individuals engaged by a business for various purposes
            - address_region (Optional[str]): The name of the geographical area for this address of the organization
            - address_country (str): Records the details of the county where the business is located.
            - yearly_revenue_value (float): The annual sales or revenue of the company.
            - industry_name (str): industry name taken from industry code
    """
    matched_candidates: List[EnrichedMatchedCompany] = []

    list_of_criteria = [
        address_region,
        address_country,
        employee_min_count,
        employee_max_count,
        revenue_min_quantity,
        revenue_max_quantity,
        ussicv4_code,
    ]
    if not any(list_of_criteria):
        # no values passed in by agent, return no matched companies
        return matched_candidates

    search_criteria: Dict[str, object] = {
        "globalUltimateCountryISOAlpha2Code": address_country,
        "locationNavigatorType": "countryISOAlpha2Code",
        "numberOfEmployees": {
            "minimumValue": employee_min_count,
            "maximumValue": employee_max_count,
        },
        "yearlyRevenue": {
            "minimumValue": revenue_min_quantity,
            "maximumValue": revenue_max_quantity,
        },
    }

    # for values with no min/max or default
    if address_region:
        search_criteria["addressRegion"] = address_region
    if ussicv4_code:
        search_criteria["usSicV4"] = [ussicv4_code]

    client = get_dnb_client(entitlement=DNBEntitlements.SALES)

    responses = []

    # temporary hack to get businesses by criteria
    for corp in CorpTypes:
        search_criteria["searchTerm"] = corp.name
        responses.append(
            client.post_request(
                version="v1", category="search", endpoint="criteria", data=search_criteria
            )
        )

    for response in responses:
        # Check if we have an error in the response.
        api_url = "https://plus.dnb.com/v1/search/criteria"
        url_params = search_criteria
        error_response = process_dnb_error(response, api_url, url_params)
        if "searchCandidates" in response:
            for candidate in response["searchCandidates"]:
                org = candidate["organization"]
                matched_candidates.append(EnrichedMatchedCompany.from_api_response(org))

    # If there is no matched_candidates, then return error_response, else return matched_candidates
    if not matched_candidates or not isinstance(matched_candidates, list):
        return error_response
    else:
        return matched_candidates
