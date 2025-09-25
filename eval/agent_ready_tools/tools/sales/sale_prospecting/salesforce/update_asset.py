from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def update_asset(
    asset_id: str,
    asset_name: Optional[str] = None,
    asset_description: Optional[str] = None,
    asset_status: Optional[str] = None,
    account_id: Optional[str] = None,
    contact_id: Optional[str] = None,
    asset_amount: Optional[int] = None,
    asset_quantity: Optional[int] = None,
) -> int:
    """
    Updates an existing asset record in Salesforce.

    Args:
        asset_id: The id of the asset to be updated, returned by `list_assets` tool in Salesforce.
        asset_name: The new name of the asset in Salesforce.
        asset_description: The new description of the asset in Salesforce.
        asset_status: The new status of the asset, returned by `list_asset_statuses` tool in
            Salesforce.
        account_id: The new id of account, returned by the tool `list_accounts` tool in Salesforce.
        contact_id: The new id of contact, returned by the tool `list_contacts` tool in Salesforce.
        asset_amount: The new amount of the asset in Salesforce.
        asset_quantity: The new quantity of the asset in Salesforce.

    Returns:
        The status of the update operation performed on the asset in Salesforce.
    """

    client = get_salesforce_client()

    data = {
        "Name": asset_name,
        "Description": asset_description,
        "Status": asset_status,
        "AccountId": account_id,
        "ContactId": contact_id,
        "Price": asset_amount,
        "Quantity": asset_quantity,
    }

    data = {key: value for key, value in data.items() if value}

    status = client.salesforce_object.Asset.update(asset_id, data)  # type: ignore[operator]

    return status
