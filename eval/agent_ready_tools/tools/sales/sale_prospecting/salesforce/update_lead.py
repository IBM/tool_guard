from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def update_lead(
    lead_id: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    description: Optional[str] = None,
    title: Optional[str] = None,
    industry: Optional[str] = None,
    status: Optional[str] = None,
) -> int:
    """
    Updates an existing lead in Salesforce.

    Args:
        lead_id: The ID of the lead to update.
        first_name: The first name of the lead.
        last_name: The last name of the lead.
        email: The email of the lead
        description: The description of the lead.
        title: The title of the lead.
        industry: The industry of the lead returned by `list_lead_industry` tool.
        status: The status of the lead returned by `list_lead_status` tool.

    Returns:
        The updated lead object.
    """
    client = get_salesforce_client()
    data = {
        "FirstName": first_name,
        "LastName": last_name,
        "Email": email,
        "Description": description,
        "Title": title,
        "Industry": industry,
        "Status": status,
    }
    data = {key: value for key, value in data.items() if value}
    response = client.salesforce_object.Lead.update(lead_id, data)  # type: ignore[operator]

    return response
