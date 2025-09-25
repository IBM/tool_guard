from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Asset
from agent_ready_tools.utils.sql_utils import format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_assets(search: Optional[str] = None) -> list[Asset]:
    """
    Retrieves a list of all assets in the Salesforce org.

    Args:
        search: The SQL where clause from LLM (to clean up).

    Returns:
        A list of all assets from Salesforce.
    """
    client = get_salesforce_client()
    cleaned_clause = format_where_input_string(search or "")
    response = client.salesforce_object.query_all_iter(
        format_soql(f"SELECT Id, Name FROM Asset {cleaned_clause}")
    )
    results: list[Asset] = []
    for asset in response:
        results.append(
            Asset(
                asset_id=asset.get("Id"),
                asset_name=asset.get("Name"),
            )
        )
    return results
