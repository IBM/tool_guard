from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class OracleCountry:
    """Represents country code details in Oracle HCM."""

    country_name: str
    country_code: str


@dataclass
class GetCountriesResponse:
    """Represents the response from getting a country codes in Oracle HCM."""

    country_names: List[OracleCountry]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_countries_oracle(country_name: Optional[str] = None) -> GetCountriesResponse:
    """
    Retrieves the list of countries in Oracle HCM.

    Args:
        country_name: The name of the country to filter results.

    Returns:
        A response containing a list of countries.
    """

    client = get_oracle_hcm_client()

    filter_expr = None
    if not country_name:
        filter_expr = f"CountryName='{country_name}'"
    response = client.get_request(entity="hcmCountriesLov", q_expr=filter_expr)
    country_names_list = [
        OracleCountry(
            country_name=country.get("CountryName"), country_code=country.get("TerritoryCode")
        )
        for country in response["items"]
    ]
    return GetCountriesResponse(country_names=country_names_list)
