from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HANACountry:
    """Represents a country in SAP S4 HANA."""

    country_code: str
    country_name: str


@dataclass
class S4HANACountriesResponse:
    """A response containing the list of countries from SAP S4 HANA."""

    countries_list: List[S4HANACountry]


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_countries(
    country_name: Optional[str] = None,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[S4HANACountriesResponse]:
    """
    Gets a list of countries details from SAP S4 HANA.

    Args:
        country_name: The name of the country.
        limit: The number of countries to retrieve.
        skip: The countries to skip for pagination.

    Returns:
        A list of countries.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    filter_expr = f"Language eq 'EN'"
    if country_name:
        filter_expr = f"Language eq 'EN' and CountryName eq '{country_name}'"

    params = {"$top": limit, "$skip": skip}

    response = client.get_request(
        entity="API_COUNTRY_SRV/A_CountryText", filter_expr=filter_expr, params=params
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    countries_list = [
        S4HANACountry(
            country_code=item.get("Country", ""),
            country_name=item.get("CountryName", ""),
        )
        for item in response["response"]["d"]["results"]
    ]

    return ToolResponse(
        success=True,
        message="The data was successfully retrieved",
        content=S4HANACountriesResponse(countries_list=countries_list),
    )
