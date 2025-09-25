from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def update_user(
    user_id: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    alias: Optional[str] = None,
    country: Optional[str] = None,
    company: Optional[str] = None,
) -> int:
    """
    Updates an existing user in Salesforce.

    Args:
        user_id: The id of the user in Salesforce returned by the tool `list_users`.
        first_name: The first name of the user in Salesforce.
        last_name: The last name of the user in Salesforce.
        alias: The alternative name of the user in Salesforce.
        country: The country of the user in Salesforce returned by the tool `list_countries`.
        company: The company name of the user in Salesforce.

    Returns:
        The result of the update operation performed on the existing user record.
    """
    client = get_salesforce_client()
    data = {
        "FirstName": first_name,
        "LastName": last_name,
        "Alias": alias,
        "CompanyName": company,
        "Country": country,
    }
    # Filter out the blank parameters.
    data = {key: value for key, value in data.items() if value}
    status = client.salesforce_object.User.update(user_id, data)  # type: ignore[operator]

    return status
