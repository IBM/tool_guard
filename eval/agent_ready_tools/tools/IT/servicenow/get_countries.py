from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class ServiceNowCountry:
    """Represents a single country object in ServiceNow."""

    country_name: str
    country_code: str


@dataclass
class CountryResponse:
    """A list of countries in ServiceNow."""

    countries_list: list[ServiceNowCountry]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_countries(
    country_name: Optional[str] = None, country_code: Optional[str] = None
) -> CountryResponse:
    """
    Retrieves a list of all countries in ServiceNow.

    Args:
        country_name: The optional parameter for retrieving the country name.
        country_code: The optional parameter for retrieving the country code.

    Returns:
        The result from all countries details.
    """

    client = get_servicenow_client()

    params = {
        "name": "sys_user",
        "element": "country",
        "label": country_name,
        "value": country_code,
    }

    params = {key: value for key, value in params.items() if value}

    response = client.get_request(entity="sys_choice", params=params)
    countries_list = [
        ServiceNowCountry(
            country_name=country.get("label", ""), country_code=country.get("value", "")
        )
        for country in response["result"]
    ]

    return CountryResponse(countries_list=countries_list)
