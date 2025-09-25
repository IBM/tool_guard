from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import (
    AccountType,
    PickListOptionsPair,
)
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_account_types() -> List[AccountType]:
    """
    Retrieves all account types from Salesforce.

    Returns:
        list of account type values are returned.
    """
    client = get_salesforce_client()
    response = client.get_picklist_options(
        PickListOptionsPair.AccountType.obj_api_name,
        PickListOptionsPair.AccountType.field_api_name,
    )

    account_type_list = [
        AccountType(account_type=value.get("value")) for value in response.get("values", [])
    ]

    return account_type_list
