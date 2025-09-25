from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import Account
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(permission=ToolPermission.WRITE_ONLY, expected_credentials=SALESFORCE_CONNECTIONS)
def create_account(
    name: str,
    account_type: Optional[str] = None,
    phone: Optional[str] = None,
    website: Optional[str] = None,
) -> Account:
    """
    Creates a new account in Salesforce.

    Args:
        name: The name of the account.
        account_type: The account type is returned by `list_account_types` helper tool in
            Salesforce.
        phone: The phone number of the account.
        website: The website of the account.

    Returns:
        Returns newly created account data in Salesforce
    """
    client = get_salesforce_client()

    # Clear any previous value
    account_obj = None

    data = {
        "Name": name,
        "Type": account_type,
        "Phone": phone,
        "Website": website,
    }
    account_obj = client.salesforce_object.Account.create(data)  # type: ignore[operator]

    account = {"id": account_obj.get("id"), "name": name}

    return Account(**account)
