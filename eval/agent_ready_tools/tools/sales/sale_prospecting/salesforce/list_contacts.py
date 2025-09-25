from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import SalesforceError, format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import Contact, ErrorResponse
from agent_ready_tools.utils.sql_utils import format_select_clause_list, format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS

FALLBACK_FIELDS = ["Id", "AccountId", "Name", "Email", "Phone", "Title", "MobilePhone"]


# TODO: after GA, create a common tool directory and place this tool there, for reuse.
#  Same functionality as `list_accounts` for salesforce productivity
@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_sales_contacts(
    default_fields: str = "",
    optional_fields: str = "",
    use_optional_fields: bool = False,
    search: Optional[str] = None,
) -> List[Contact] | ErrorResponse:
    """
    Searches for Salesforce contacts using a search query with optional filters.

    Optional filters: account id, email, phone, name, title.

    Args:
        default_fields: Default fields to query.
        optional_fields: Set of optional fields to query on request.
        use_optional_fields: A flag to use the optional fields in the query.
        search: The SQL where clause from LLM (to clean up).

    Returns:
        A list of Contact objects.
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
            format_soql(f"SELECT {cleaned_select_clause} FROM Contact {cleaned_where_clause}")
        )

        results: List[Contact] = []
        for row in rs:
            additional_data = {
                key: value
                for key, value in row.items()
                if key not in [*FALLBACK_FIELDS, "attributes"]
            }
            results.append(
                Contact(
                    mobile_phone=row.get("MobilePhone", ""),
                    account_id=row.get("AccountId", ""),
                    id=row.get("Id"),
                    name=row.get("Name"),
                    email=row.get("Email"),
                    phone=row.get("Phone"),
                    title=row.get("Title"),
                    additional_data=additional_data if additional_data else None,
                )
            )
        return results
    except SalesforceError as err:
        return ErrorResponse(
            message=str(err),
            payload={search},
            status_code=err.status,
        )
