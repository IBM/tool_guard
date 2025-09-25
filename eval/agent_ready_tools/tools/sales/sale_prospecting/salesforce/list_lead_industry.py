from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import (
    LeadIndustry,
    PickListOptionsPair,
)
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_lead_industry() -> List[LeadIndustry]:
    """
    Retrieves a list of lead industries in Salesforce.

    Returns:
        List of lead industries are returned.
    """
    client = get_salesforce_client()
    response = client.get_picklist_options(
        PickListOptionsPair.LeadIndustry.obj_api_name,
        PickListOptionsPair.LeadIndustry.field_api_name,
    )

    lead_industry_list = [
        LeadIndustry(lead_industry=value.get("value")) for value in response.get("values", [])
    ]

    return lead_industry_list
