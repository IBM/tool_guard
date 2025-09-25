from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def update_account(
    account_id: str,
    account_name: Optional[str] = None,
    account_type: Optional[str] = None,
    description: Optional[str] = None,
    number_of_employees: Optional[str] = None,
    annual_revenue: Optional[str] = None,
    owner_id: Optional[str] = None,
) -> int:
    """
    Updates an existing account in Salesforce.

    Args:
        account_id: The id of the account in Salesforce returned by the `list_accounts` tool.
        account_name: The name of the account in Salesforce.
        account_type: The type of the account in Salesforce returned by the `list_accounts_types`
            tool.
        description: The description of the account in salesforce.
        number_of_employees: The number of employees associated with the account in Salesforce.
        annual_revenue: The annual revenue of the account in Salesforce.
        owner_id: The owner id of the account in Salesforce returned by the `list_users` tool

    Returns:
        The status code of the update operation performed on the API.
    """
    client = get_salesforce_client()
    data = {
        "Name": account_name,
        "Type": account_type,
        "Description": description,
        "NumberOfEmployees": number_of_employees,
        "AnnualRevenue": annual_revenue,
        "OwnerId": owner_id,
    }

    data = {key: value for key, value in data.items() if value}

    status_code = client.salesforce_object.Account.update(account_id, data)  # type: ignore[operator]

    return status_code
