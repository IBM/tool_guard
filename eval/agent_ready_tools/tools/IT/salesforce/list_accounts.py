from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import SalesforceError, format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import Account, ErrorResponse
from agent_ready_tools.utils.sql_utils import format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_accounts(search: Optional[str] = None) -> list[Account] | ErrorResponse:
    """
    Searches for Salesforce accounts using a search query with zero, one, or more of the optional
    filters: industry, ID, name.

    Args:
        search: The SQL where clause from LLM (to clean up).

    Returns:
        A list of Account objects.
    """
    client = get_salesforce_client()
    cleaned_clause = format_where_input_string(search or "")

    try:
        rs = client.salesforce_object.query_all_iter(
            format_soql(f"SELECT Id, Name, Industry FROM Account {cleaned_clause}")
        )
        results: list[Account] = []
        for row in rs:
            account_id = row.get("Id")
            account_name = row.get("Name")
            account_industry = row.get("Industry")
            results.append(Account(id=account_id, name=account_name, industry=account_industry))
        return results
    except SalesforceError as err:
        return ErrorResponse(message=str(err), status_code=err.status, payload={search})
