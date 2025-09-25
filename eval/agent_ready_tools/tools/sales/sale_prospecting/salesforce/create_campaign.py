from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@dataclass
class CreateCampaignResponse:
    """Respresents the result of creating an campaign in Salesforce."""

    campaign_id: str


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def create_campaign(
    campaign_name: str,
    campaign_type: Optional[str] = None,
    campaign_status: Optional[str] = None,
    campaign_description: Optional[str] = None,
    campaign_start_date: Optional[str] = None,
    campaign_end_date: Optional[str] = None,
) -> CreateCampaignResponse:
    """
    Creates a new campaign in Salesforce.

    Args:
        campaign_name: The name of the campaign.
        campaign_type: The type of the campaign returned by `get_campaign_type` tool.
        campaign_status: The status of the campaign returned by `get_campaign_status` tool.
        campaign_description: The description of the campaign.
        campaign_start_date: The start date of the campaign in ISO 8601 format (e.g., YYYY-MM-DD).
        campaign_end_date: The end date of the campaign in ISO 8601 format (e.g., YYYY-MM-DD).

    Returns:
        The ID of the created campaign.
    """
    client = get_salesforce_client()

    data = {
        "Name": campaign_name,
        "Type": campaign_type,
        "Status": campaign_status,
        "Description": campaign_description,
        "StartDate": campaign_start_date,
        "EndDate": campaign_end_date,
    }

    response = client.salesforce_object.Campaign.create(data)  # type: ignore[operator]

    return CreateCampaignResponse(
        campaign_id=response.get(
            "id",
        )
    )
