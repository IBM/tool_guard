from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import CaseType, PickListOptionsPair
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(permission=ToolPermission.READ_ONLY, expected_credentials=SALESFORCE_CONNECTIONS)
def list_case_type() -> List[CaseType]:
    """
    Retrieves a list of all case types values in Salesforce.

    Returns:
        list of case type values are returned.
    """
    client = get_salesforce_client()
    response = client.get_picklist_options(
        PickListOptionsPair.CaseType.obj_api_name, PickListOptionsPair.CaseType.field_api_name
    )
    case_type_list = [
        CaseType(case_type=value.get("value")) for value in response.get("values", [])
    ]

    return case_type_list
