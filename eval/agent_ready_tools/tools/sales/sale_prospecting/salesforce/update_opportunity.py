from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def update_opportunity(
    opportunity_id: str,
    name: Optional[str] = None,
    amount: Optional[float] = None,
    close_date: Optional[str] = None,
    stage_name: Optional[str] = None,
    description: Optional[str] = None,
    opportunity_type: Optional[str] = None,
    lead_source: Optional[str] = None,
) -> int:
    """
    Updates an existing opportunity in Salesforce.

    Args:
        opportunity_id: The ID of the opportunity to update.
        name: The name of the opportunity.
        amount: The amount of the opportunity.
        close_date: The close date of the opportunity.
        stage_name: The stage of the opportunity.
        description: The description of the opportunity.
        opportunity_type: The type of the opportunity.
        lead_source: The lead source of the opportunity.

    Returns:
        The status of the update operation performed on the opportunity.
    """
    client = get_salesforce_client()
    data = {
        "Name": name,
        "Amount": amount,
        "CloseDate": close_date,
        "StageName": stage_name,
        "Description": description,
        "Type": opportunity_type,
        "LeadSource": lead_source,
    }
    data = {key: value for key, value in data.items() if value}
    response = client.salesforce_object.Opportunity.update(opportunity_id, data)  # type: ignore[operator]

    return response
