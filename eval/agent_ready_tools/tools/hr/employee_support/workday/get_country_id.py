from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_country_id(country_name: str) -> Optional[str]:
    """
    Get the country id used to identify a country in Workday.

    Args:
        country_name: The name of the country.

    Returns:
        country_id corresponding to the country.
    """
    client = get_workday_client()
    url = f"api/person/v4/{client.tenant_name}/values/countryComponents/country/"
    response = client.get_request(url=url)
    all_countries = response["data"]
    for country in all_countries:
        if country["descriptor"].strip().lower() == country_name.strip().lower():
            return country["id"]
    return None
