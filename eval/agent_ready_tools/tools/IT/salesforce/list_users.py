from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import User
from agent_ready_tools.utils.sql_utils import format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_users(search: Optional[str] = None) -> List[User]:
    """
    Retrieves the list of users from Salesforce.

    Args:
        search: The SQL where clause from LLM (to clean up).

    Returns:
        A list of users from Salesforce.
    """
    client = get_salesforce_client()
    cleaned_clause = format_where_input_string(search or "")
    rs = client.salesforce_object.query_all_iter(
        format_soql(f"SELECT Id, Name, Alias, Email, Phone, State FROM User {cleaned_clause}")
    )

    results: List[User] = []
    for row in rs:
        results.append(
            User(
                user_id=row.get("Id", ""),
                name=row.get("Name", ""),
                alias=row.get("Alias", ""),
                email=row.get("Email", ""),
                phone_number=row.get("Phone", ""),
                state=row.get("State", ""),
            )
        )
    return results
