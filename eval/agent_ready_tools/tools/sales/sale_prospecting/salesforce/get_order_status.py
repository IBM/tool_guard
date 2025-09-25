from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Status
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def get_order_status() -> list[Status]:
    """
    Returns a list of status objects for the orders in the Salesforce org.

    Returns:
        A list of Status objects.
    """
    client = get_salesforce_client()

    rs = client.salesforce_object.Order.describe()  # type: ignore[operator]

    status_field = next(
        field for field in rs.get("fields", "") if field.get("name", "") == "StatusCode"
    )
    picklist_values = status_field["picklistValues"]

    status_list: List[Status] = [
        Status(
            value=entry.get("value", ""),
            label=entry.get("label", ""),
            active=entry.get("active", ""),
        )
        for entry in picklist_values
    ]

    return status_list
