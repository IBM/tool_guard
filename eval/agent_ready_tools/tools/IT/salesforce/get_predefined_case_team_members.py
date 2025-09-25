from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import PredefinedCaseTeamMember
from agent_ready_tools.utils.sql_utils import format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(permission=ToolPermission.READ_ONLY, expected_credentials=SALESFORCE_CONNECTIONS)
def get_predefined_case_team_members(
    search: Optional[str] = None,
) -> List[PredefinedCaseTeamMember]:
    """
    Searches for Salesforce predefined case team members using a search query with zero, one, or more of the optional
    filters: ID, member id, creation date, team template id.

    Args:
        search: The SQL where clause from LLM (to clean up).

    Returns:
        List of predefined case team members.
    """
    client = get_salesforce_client()

    results: List[PredefinedCaseTeamMember] = []

    cleaned_clause = format_where_input_string(search or "")

    rs = client.salesforce_object.query_all_iter(
        format_soql(
            f"SELECT Id, MemberId, CreatedDate, TeamTemplateId FROM CaseTeamTemplateMember {cleaned_clause}"
        )
    )

    for obj in rs:
        results.append(
            PredefinedCaseTeamMember(
                id=obj.get("Id"),
                member_id=obj.get("MemberId"),
                created_date=obj.get("CreatedDate"),
                team_template_id=obj.get("TeamTemplateId"),
            )
        )

    return results
