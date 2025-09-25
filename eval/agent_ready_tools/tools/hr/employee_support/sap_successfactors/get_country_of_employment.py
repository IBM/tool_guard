from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class CountryOfEmployment:
    """Represents the country of employment of a user in SAP SuccessFactors."""

    country_of_employment: str


@dataclass
class CountryOfEmploymentResponse:
    """Represents the response from getting a user's country in SAP SuccessFactors."""

    countries_of_employment: List[CountryOfEmployment]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_country_of_employment(user_id: str) -> CountryOfEmploymentResponse:
    """
    Gets a user's country of employment in SAP SuccessFactors.

    Args:
        user_id: The user's id uniquely identifying them within the SuccessFactors API.

    Returns:
        The 3-letter ISO code of the user's country of employment.
    """
    client = get_sap_successfactors_client()

    response = client.get_request(entity="EmpJob", filter_expr=f"userId eq '{user_id}'")

    countries_of_employment: list[CountryOfEmployment] = []
    for result in response["d"]["results"]:
        countries_of_employment.append(
            CountryOfEmployment(country_of_employment=result.get("countryOfCompany"))
        )
    return CountryOfEmploymentResponse(countries_of_employment=countries_of_employment)
