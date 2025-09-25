from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import (
    LeadStatus,
    PickListOptionsPair,
)
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_lead_status() -> List[LeadStatus]:
    """
    Retrieves a list of lead status values in Salesforce.

    Returns:
        List of lead status values are returned.
    """
    client = get_salesforce_client()
    response = client.get_picklist_options(
        PickListOptionsPair.LeadStatus.obj_api_name,
        PickListOptionsPair.LeadStatus.field_api_name,
    )

    lead_status_list = [
        LeadStatus(lead_status=value.get("value")) for value in response.get("values", [])
    ]

    return lead_status_list
