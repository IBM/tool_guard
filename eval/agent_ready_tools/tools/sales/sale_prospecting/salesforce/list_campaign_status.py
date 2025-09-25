from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import (
    CampaignStatus,
    PickListOptionsPair,
)
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_campaign_status() -> List[CampaignStatus]:
    """
    Retrieves a list of all campaign statuses in Salesforce.

    Returns:
        List of campaign status values.
    """
    client = get_salesforce_client()

    response = client.get_picklist_options(
        PickListOptionsPair.CampaignStatus.obj_api_name,
        PickListOptionsPair.CampaignStatus.field_api_name,
    )

    campaign_status_list = [
        CampaignStatus(campaign_status=value.get("value")) for value in response.get("values", [])
    ]

    return campaign_status_list
