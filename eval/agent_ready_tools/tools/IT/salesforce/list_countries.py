from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import Country, PickListOptionsPair
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS

_RECORD_TYPE_ID: Optional[str] = "012000000000000AAA"


@tool(permission=ToolPermission.READ_ONLY, expected_credentials=SALESFORCE_CONNECTIONS)
def list_countries() -> List[Country]:
    """
    Retrieves a list of all countries in Salesforce.

    Returns:
        List of country values are returned.
    """
    client = get_salesforce_client()
    response = client.get_picklist_options(
        PickListOptionsPair.Country.obj_api_name,
        PickListOptionsPair.Country.field_api_name,
        _RECORD_TYPE_ID,
    )

    country_list = [
        Country(country_name=value.get("label"), country_code=value.get("value"))
        for value in response.get("values", [])
    ]

    return country_list
