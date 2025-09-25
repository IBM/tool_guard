from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass
from simple_salesforce.exceptions import SalesforceError

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@dataclass
class DeleteAssetResponse:
    """Represents the result of delete an asset operation in Salesforce."""

    http_code: int


@tool(permission=ToolPermission.WRITE_ONLY, expected_credentials=SALESFORCE_CONNECTIONS)
def delete_an_asset(asset_id: str) -> DeleteAssetResponse:
    """
    Deletes an asset in Salesforce.

    Args:
        asset_id: The asset_id uniquely identifying the asset, returned by `list_assets` tool.

    Returns:
        The result of performing the delete operation on an asset.
    """

    client = get_salesforce_client()

    http_code = None

    try:
        response = client.salesforce_object.Asset.delete(asset_id)  # type: ignore[operator]
        http_code = response.status_code if hasattr(response, "status_code") else response
    except SalesforceError as err:
        http_code = err.status

    return DeleteAssetResponse(http_code)
