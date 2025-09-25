from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import CaseTeam
from agent_ready_tools.utils.sql_utils import format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(permission=ToolPermission.READ_ONLY, expected_credentials=SALESFORCE_CONNECTIONS)
def get_predefined_case_teams(search: Optional[str] = None) -> List[CaseTeam]:
    """
    Searches for Salesforce predefined case teams using a search query with zero, one, or more of the optional
    filters: description, ID, name, creation date.

    Args:
        search: The SQL where clause from LLM (to clean up).

    Returns:
        List of predefined case teams.
    """
    client = get_salesforce_client()

    results: List[CaseTeam] = []

    cleaned_clause = format_where_input_string(search or "")

    rs = client.salesforce_object.query_all_iter(
        format_soql(
            f"SELECT Id, Name, CreatedDate, Description FROM CaseTeamTemplate {cleaned_clause}"
        )
    )

    for obj in rs:
        results.append(
            CaseTeam(
                team_template_id=obj.get("Id"),
                name=obj.get("Name"),
                created_date=obj.get("CreatedDate"),
                description=obj.get("Description", ""),
            )
        )

    return results
