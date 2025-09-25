from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass
from simple_salesforce.exceptions import SalesforceError

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@dataclass
class DeleteCampaignResponse:
    """Represents the response of deleting a campaign in Salesforce."""

    http_code: int


@tool(permission=ToolPermission.WRITE_ONLY, expected_credentials=SALESFORCE_CONNECTIONS)
def delete_campaign(campaign_id: str) -> DeleteCampaignResponse:
    """
    Deletes a campaign in Salesforce.

    Args:
        campaign_id: The id of the campaign returned by the `get_campaign` tool.

    Returns:
        Confirmation of the comment deletion.
    """

    client = get_salesforce_client()

    http_code = None

    try:
        response = client.salesforce_object.Campaign.delete(campaign_id)  # type: ignore[operator]
        http_code = response.status_code if hasattr(response, "status_code") else response

    except SalesforceError as err:
        http_code = err.status

    return DeleteCampaignResponse(http_code=http_code)
