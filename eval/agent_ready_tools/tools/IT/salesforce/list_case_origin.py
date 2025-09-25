from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import CaseOrigin, PickListOptionsPair
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(permission=ToolPermission.READ_ONLY, expected_credentials=SALESFORCE_CONNECTIONS)
def list_case_origin() -> List[CaseOrigin]:
    """
    Retrieves a list of all case origin values in Salesforce.

    Returns:
        list of case origin values are returned.
    """
    client = get_salesforce_client()
    response = client.get_picklist_options(
        PickListOptionsPair.CaseOrigin.obj_api_name, PickListOptionsPair.CaseOrigin.field_api_name
    )
    case_origin_list = [
        CaseOrigin(case_origin=value.get("value")) for value in response.get("values", [])
    ]

    return case_origin_list
