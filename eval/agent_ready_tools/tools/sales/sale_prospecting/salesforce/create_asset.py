from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@dataclass
class CreateAssetResponse:
    """Respresents the result of creating an asset in Salesforce."""

    asset_id: str


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def create_asset(
    account_id: str,
    contact_id: str,
    asset_name: str,
    asset_amount: Optional[int] = None,
    asset_status: Optional[str] = None,
    asset_quantity: Optional[int] = None,
    asset_description: Optional[str] = None,
) -> CreateAssetResponse:
    """
    Creates an asset in Salesforce.

    Args:
        account_id: The id of the parent account, returned by the tool `list_accounts` tool.
        contact_id: The id of the contact, returned by the tool `list_contacts` tool.
        asset_name: The name of the asset in Salesforce.
        asset_amount: The amount of the asset in Salesforce.
        asset_status: The order status of the asset, returned by the tool `list_asset_statuses`.
        asset_quantity: The quantity of the asset in Salesforce.
        asset_description: The description of the asset in Salesforce.

    Returns:
        The result of create operation of an asset.
    """

    client = get_salesforce_client()

    payload = {
        "AccountId": account_id,
        "ContactId": contact_id,
        "Name": asset_name,
        "Price": asset_amount,
        "Status": asset_status,
        "Quantity": asset_quantity,
        "Description": asset_description,
    }

    response = client.salesforce_object.Asset.create(data=payload)  # type: ignore[operator]

    return CreateAssetResponse(asset_id=response.get("id"))
