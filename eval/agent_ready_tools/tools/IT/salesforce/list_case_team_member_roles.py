from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import CaseTeamRole
from agent_ready_tools.utils.sql_utils import format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_case_team_member_roles(
    search: Optional[str] = None,
) -> List[CaseTeamRole]:
    """
    Searches for Salesforce case team member roles using a search query with zero, one, or more of the optional
    filters: ID, name, access level, creation date.

    Args:
        search: The SQL where clause from LLM (to clean up).

    Returns:
        A list of case team member roles from Salesforce.
    """

    client = get_salesforce_client()
    cleaned_clause = format_where_input_string(search or "")
    response = client.salesforce_object.query_all_iter(
        format_soql(f"SELECT Id, Name, AccessLevel, CreatedDate FROM CaseTeamRole {cleaned_clause}")
    )

    results: list[CaseTeamRole] = []
    for record in response:
        case_team_member_role_id = record.get("Id")
        case_team_member_role_name = record.get("Name")
        access_level = record.get("AccessLevel")
        created_date = record.get("CreatedDate")
        results.append(
            CaseTeamRole(
                case_team_member_role_id=case_team_member_role_id,
                case_team_member_role_name=case_team_member_role_name,
                access_level=access_level,
                created_date=created_date,
            )
        )
    return results
