from typing import Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.format_tool_input import string_to_list_of_strings
from agent_ready_tools.utils.tool_credentials import DNB_PROCUREMENT_CONNECTIONS


@dataclass
class MatchedCompanyDetails:
    """Dataclass representing a company response from DnB."""

    duns_number: Optional[str] = None
    primary_name: Optional[str] = None
    address_country: Optional[str] = None
    website: Optional[str] = None


@tool(expected_credentials=DNB_PROCUREMENT_CONNECTIONS)
def dnb_search_company_by_sic(
    ussicv4_code: List[str],
    address_country: str = "US",
    address_region: Optional[str] = None,
    employee_min_count: Optional[int] = 1,
    employee_max_count: int = 999999,
    revenue_min_quantity: Optional[int] = 1,
    revenue_max_quantity: int = 100000000000000,
) -> ToolResponse[List[MatchedCompanyDetails]]:
    """
    Searches for companies by SIC code using specified criteria.

    Args:
        ussicv4_code: US SIC V4 code(s) as a a comma sepatated string
        address_country: Two-letter country code (default: "US").
        address_region: The region of the company's address.
        employee_min_count: Minimum number of employees.
        employee_max_count: Maximum number of employees.
        revenue_min_quantity: Minimum revenue quantity.
        revenue_max_quantity: Maximum revenue quantity.

    Returns:
        A list of matched suppliers.
    """

    if isinstance(ussicv4_code, str):
        ussicv4_code = string_to_list_of_strings(ussicv4_code)
    # Process ussicv4_code into a list of strings.
    final_ussicv4_code: List[str] = []
    if len(ussicv4_code) > 0:
        final_ussicv4_code = [
            code for code in map(str.strip, ussicv4_code) if code.isdigit() and len(code) == 4
        ]
    # Build the search criteria payload.
    search_criteria: Dict[str, object] = {
        "countryISOAlpha2Code": address_country,
    }

    if employee_min_count and employee_max_count:
        search_criteria["numberOfEmployees"] = {
            "minimumValue": employee_min_count,
            "maximumValue": employee_max_count,
        }
    if revenue_min_quantity and revenue_max_quantity:
        search_criteria["yearlyRevenue"] = {
            "minimumValue": revenue_min_quantity,
            "maximumValue": revenue_max_quantity,
        }

    if address_region:
        search_criteria["addressRegion"] = address_region
    if final_ussicv4_code:
        search_criteria["usSicV4"] = final_ussicv4_code

    try:
        client = get_dnb_client(entitlement=DNBEntitlements.PROCUREMENT)
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrive credentials")

    response = client.post_request(
        version="v1", category="search", endpoint="criteria", data=search_criteria
    )
    if "error" in response and "errorMessage" in response["error"]:
        return ToolResponse(success=False, message=response["error"]["errorMessage"])

    if "searchCandidates" not in response:
        return ToolResponse(success=False, message="No company was matched with your query")

    matched_companies: List[MatchedCompanyDetails] = []

    for candidate in response["searchCandidates"]:
        organization = candidate.get("organization", {})
        duns = organization.get("duns")
        primary_name = organization.get("primaryName")
        address_country = organization.get("primaryAddress", {}).get("addressCountry")
        website = organization.get("domain")
        if duns and primary_name:
            matched_companies.append(
                MatchedCompanyDetails(
                    duns_number=duns,
                    primary_name=primary_name,
                    address_country=address_country,
                    website=website,
                )
            )

    return ToolResponse(
        success=True, message="The data was successfully retrieved", content=matched_companies
    )
