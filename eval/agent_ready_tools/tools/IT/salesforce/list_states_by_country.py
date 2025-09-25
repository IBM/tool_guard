from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import PickListOptionsPair, State
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_states_by_country(country_code: str) -> List[str]:
    """
    Retrieves the list of all states based on the country in Salesforce.

    Args:
        country_code: The code of the country is returned by 'list_countries' tool.

    Returns:
        List of states based on the country are returned.
    """

    client = get_salesforce_client()
    response = client.get_picklist_options(
        PickListOptionsPair.Contact.obj_api_name, PickListOptionsPair.Contact.field_api_name
    )
    country_value = response.get("controllerValues", {}).get(country_code, "")
    state_list = [
        State(state=value.get("label"), valid_for=value.get("validFor", "")).state
        for value in response.get("values", [])
        if country_value in value.get("validFor", [])
    ]

    return state_list
