from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import Role
from agent_ready_tools.utils.sql_utils import format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_roles(
    search: Optional[str] = None, limit: Optional[int] = 100, offset: Optional[int] = 0
) -> list[Role]:
    """
    Retrieves user roles from Salesforce.

    Args:
        search: The SQL where clause from LLM (to clean up).
        limit: The maximum number of roles to retrieve.default is 100.
        offset: The number of records to skip before starting to return results.default is 0.

    Returns:
        A list of user roles from Salesforce.
    """

    client = get_salesforce_client()

    cleaned_clause = format_where_input_string(search or "")

    rs = client.salesforce_object.query_all_iter(
        format_soql(
            f"SELECT Id, Name, ParentRoleId, DeveloperName, ForecastUserId FROM UserRole {cleaned_clause} LIMIT {limit} OFFSET {offset}"
        )
    )

    # Extract user role values
    user_roles: list[Role] = []
    for record in rs:
        user_roles.append(
            Role(
                role_id=record.get("Id", ""),
                role_name=record.get("Name", ""),
                parent_role_id=record.get("ParentRoleId", ""),
                developer_name=record.get("DeveloperName", ""),
                forecast_user_id=record.get("ForecastUserId", ""),
            )
        )
    return user_roles
