from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.zoominfo_client import get_zoominfo_client
from agent_ready_tools.tools.sales.sales_research.zoominfo.zoominfo_schemas import ErrorResponse
from agent_ready_tools.utils.tool_credentials import ZOOMINFO_CONNECTIONS


@dataclass
class ZoominfoCompany:
    """Dataclass representing on search company from Zoominfo."""

    company_id: int  # mapped from companyId
    company_name: str  # mapped from companyName


@tool(expected_credentials=ZOOMINFO_CONNECTIONS)
def zoominfo_search_company_by_criteria(
    company_id: Optional[int] = None,
    company_name: Optional[str] = None,
    revenue_min: int = 0,
    revenue_max: int = 9999999999999,
    employee_count_min: Optional[str] = None,
    employee_count_max: Optional[str] = None,
    state: Optional[str] = None,
    country: Optional[str] = None,
    industry_keywords: Optional[str] = None,
) -> List[ZoominfoCompany] | ErrorResponse:
    """
    Retrieves company information based on specific search fields from Zoominfo API.

    Args:
        company_id: ZoomInfo unique identifier for the company.
        company_name: Company Name.
        revenue_min: Minimuim yearly revenue for the company in 1000's
        revenue_max: Maximum yearly revenue for the company in 1000's
        employee_count_min: Minimum number of people employed by the company.
        employee_count_max: Maximum number of people employed by the company.
        state: Company state (U.S.) or province (Canada).
        country: Country for the company's primary address.
        industry_keywords: industry keywords associated with a company.

    Returns:
        A list of company objects returned from the search. Each object includes:
            - company_id (Optional[str]): ZoomInfo unique identifier for the company.
            - company_name (Optional[str]): The company name that the contact works for.
    """
    client = get_zoominfo_client()

    response = client.post_request(
        category="search",
        endpoint="company",
        data={
            "companyId": company_id,
            "companyName": company_name,
            "revenueMin": revenue_min,
            "revenueMax": revenue_max,
            "employeeRangeMin": employee_count_min,
            "employeeRangeMax": employee_count_max,
            "state": state,
            "country": country,
            "industryKeywords": industry_keywords,
        },
    )
    if "error" not in response:
        company_data = response.get("data", None)

        results: list[ZoominfoCompany] = []
        if company_data:
            for company in company_data:
                results.append(
                    ZoominfoCompany(
                        company_id=company.get("id", ""),
                        company_name=company.get("name", ""),
                    )
                )
        return results
    else:
        return ErrorResponse(message=response.get("error"), status_code=response.get("statusCode"))
