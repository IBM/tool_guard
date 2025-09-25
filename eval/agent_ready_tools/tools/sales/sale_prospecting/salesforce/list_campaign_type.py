from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import (
    CampaignType,
    PickListOptionsPair,
)
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_campaign_type() -> List[CampaignType]:
    """
    Retrieves a list of all campaign types in Salesforce.

    Returns:
        Campaign types for the given record type.
    """

    client = get_salesforce_client()

    response = client.get_picklist_options(
        PickListOptionsPair.CampaignStatus.obj_api_name,
        PickListOptionsPair.CampaignStatus.field_api_name,
    )

    campaign_type_list = [
        CampaignType(campaign_type=value.get("value")) for value in response.get("values", [])
    ]

    return campaign_type_list
