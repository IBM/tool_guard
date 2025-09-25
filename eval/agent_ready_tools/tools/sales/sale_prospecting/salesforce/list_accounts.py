from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import SalesforceError, format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import Account, ErrorResponse
from agent_ready_tools.utils.sql_utils import format_select_clause_list, format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS

FALLBACK_FIELDS = ["Id", "Name", "Industry"]


# TODO: after GA, create a common tool directory and place this tool there, for reuse.
#  Same functionality as `list_accounts` for salesforce productivity
@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_sales_accounts(
    default_fields: str = "",
    optional_fields: str = "",
    use_optional_fields: bool = False,
    search: Optional[str] = None,
) -> list[Account] | ErrorResponse:
    """
    Searches for Salesforce accounts using a search query with optional filters.

    Optional filters: industry, ID, name.

    Args:
        default_fields: Default fields to query.
        optional_fields: Set of optional fields to query on request.
        use_optional_fields: A flag to use the optional fields in the query.
        search: The SQL where clause from LLM (to clean up).

    Returns:
        A list of Account objects.
    """

    client = get_salesforce_client()

    select_fields_list = []

    if default_fields:
        select_fields_list.extend(default_fields.split(","))
    else:
        select_fields_list.extend(FALLBACK_FIELDS)

    if use_optional_fields:
        select_fields_list.extend(optional_fields.split(","))

    all_fields = format_select_clause_list(select_fields_list)
    cleaned_select_clause = ", ".join(all_fields)
    cleaned_where_clause = format_where_input_string(search or "")
    try:
        rs = client.salesforce_object.query_all_iter(
            format_soql(f"SELECT {cleaned_select_clause} FROM Account {cleaned_where_clause}")
        )
        results: list[Account] = []
        for row in rs:
            additional_data = {
                key: value
                for key, value in row.items()
                if key not in [*FALLBACK_FIELDS, "attributes"]
            }
            results.append(
                Account(
                    id=row.get("Id"),
                    name=row.get("Name"),
                    industry=row.get("Industry"),
                    additional_data=additional_data if additional_data else None,
                )
            )
        return results
    except SalesforceError as err:
        return ErrorResponse(message=str(err), status_code=err.status, payload={search})
