from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Campaign
from agent_ready_tools.utils.date_conversion import iso_8601_datetime_convert_to_date
from agent_ready_tools.utils.sql_utils import format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS

tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)


def list_campaigns(search: Optional[str] = None) -> list[Campaign]:
    """
    Returns a list of Campaign objects that match the given query.

    Args:
        search: The SQL where clause from LLM (to clean up).

    Returns:
        A list of Campaign objects that match the query.
    """
    client = get_salesforce_client()
    cleaned_clause = format_where_input_string(search or "")

    rs = client.salesforce_object.query_all_iter(
        format_soql(
            f"SELECT Id, Name, Status, Type, CreatedDate, StartDate, EndDate FROM Campaign {cleaned_clause}"
        )
    )

    results: list[Campaign] = []
    for obj in rs:
        data = {
            "campaign_id": obj.get("Id", ""),
            "campaign_name": obj.get("Name", ""),
            "campaign_status": obj.get("Status", ""),
            "campaign_type": obj.get("Type", ""),
            "campaign_created_date": iso_8601_datetime_convert_to_date(obj.get("CreatedDate", "")),
            "campaign_start_date": obj.get("StartDate", ""),
            "campaign_end_date": obj.get("EndDate", ""),
        }
        results.append(Campaign(**data))
    return results
