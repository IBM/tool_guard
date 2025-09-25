from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import CaseTeamMember
from agent_ready_tools.utils.sql_utils import format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_case_team_members(search: Optional[str] = None) -> list[CaseTeamMember]:
    """
    Returns a list of case team member objects in Salesforce.

    Args:
        search: The SQL where clause from LLM (to clean up).

    Returns:
        A list of case team member objects.
    """
    client = get_salesforce_client()
    cleaned_clause = format_where_input_string(search or "")

    rs = client.salesforce_object.query_all_iter(
        format_soql(
            f"SELECT Id, ParentId, MemberId, TeamRoleId, CreatedDate, CreatedById FROM CaseTeamMember {cleaned_clause}"
        )
    )

    results: list[CaseTeamMember] = []
    for record in rs:
        data = {
            "case_team_member_id": record.get("Id", ""),
            "case_id": record.get("ParentId", ""),
            "member_id": record.get("MemberId", ""),
            "team_role_id": record.get("TeamRoleId", ""),
            "create_date": record.get("CreatedDate", ""),
            "created_by_id": record.get("CreatedById", ""),
        }
        results.append(CaseTeamMember(**data))
    return results
