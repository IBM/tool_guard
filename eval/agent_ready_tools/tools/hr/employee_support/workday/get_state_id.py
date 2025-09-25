from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_state_id(country_id: str, state_name: str) -> Optional[str]:
    """
    Get the state id used to identify a state in Workday.

    Args:
        country_id: The country_id of the country to which the state belongs.
        state_name: The name of the state.

    Returns:
        state_id corresponding to the state.
    """
    client = get_workday_client()
    url = f"api/person/v4/{client.tenant_name}/values/countryComponents/countryRegion"
    params = {"country": country_id}
    response = client.get_request(url=url, params=params)
    all_countries = response["data"]
    for country in all_countries:
        if country["descriptor"].strip().lower() == state_name.strip().lower():
            return country["id"]
    return None
