from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def update_campaign(
    campaign_id: str,
    campaign_name: str,
    campaign_description: Optional[str] = None,
    campaign_is_active: Optional[bool] = False,
    campaign_type: Optional[str] = None,
    campaign_status: Optional[str] = None,
    campaign_start_date: Optional[str] = None,
    campaign_end_date: Optional[str] = None,
    campaign_expected_revenue: Optional[int] = 0,
    campaign_budgeted_cost: Optional[int] = 0,
    campaign_actual_cost: Optional[int] = 0,
    campaign_expected_response: Optional[float] = 0.0,
    campaign_number_sent: Optional[int] = 0,
    parent_campaign_id: Optional[str] = None,
) -> int:
    """
    Updates an existing campaign in Salesforce.

    Args:
        campaign_id: The id of the campaign in Salesforce returned by the tool `list_campaigns`.
        campaign_name: The name of the campaign in Salesforce.
        campaign_description: The description of the campaign in Salesforce.
        campaign_is_active: The active status of the campaign in Salesforce.
        campaign_type: The type of the campaign in Salesforce returned by the tool
            `list_campaign_type`.
        campaign_status: The status of the campain in Salesforce returned by the tool
            `list_campaign_status`.
        campaign_start_date: The start date of the campaign in Salesforce in ISO 8601 format (e.g.,
            YYYY-MM-DD).
        campaign_end_date: The end date of the campaign in Salesforce in ISO 8601 format (e.g.,
            YYYY-MM-DD).
        campaign_expected_revenue: The expected revenue of the campaign in Salesforce.
        campaign_budgeted_cost: The budgeted cost of the campaign in Salesforce.
        campaign_actual_cost: The actual cost of the campaign in Salesforce.
        campaign_expected_response: The expected response of the campaign in Salesforce.
        campaign_number_sent: The number sent for the campaign in Salesforce.
        parent_campaign_id: The parent campaign of the campaign in Salesforce returned by the tool
            `list_campaigns`.

    Returns:
        The status of the update operation performed on the campaign.
    """
    client = get_salesforce_client()
    data = {
        "Name": campaign_name,
        "ParentId": parent_campaign_id,
        "Type": campaign_type,
        "Status": campaign_status,
        "StartDate": campaign_start_date,
        "EndDate": campaign_end_date,
        "ExpectedRevenue": campaign_expected_revenue,
        "BudgetedCost": campaign_budgeted_cost,
        "ActualCost": campaign_actual_cost,
        "ExpectedResponse": campaign_expected_response,
        "NumberSent": campaign_number_sent,
        "IsActive": campaign_is_active,
        "Description": campaign_description,
    }
    # Filter out the blank parameters.
    data = {key: value for key, value in data.items() if value}
    status = client.salesforce_object.Campaign.update(campaign_id, data)  # type: ignore[operator]

    return status
