from typing import Any

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(permission=ToolPermission.WRITE_ONLY, expected_credentials=SALESFORCE_CONNECTIONS)
def update_case_team_member(case_team_member_id: str, case_team_member_role_id: str) -> int:
    """
    Updates a case team member in Salesforce.

    Args:
        case_team_member_id: The unique id of the case team member obtained from
            `list_case_team_members` tool.
        case_team_member_role_id: The unique id of the team role obtained from
            `list_case_team_member_roles` tool.

    Returns:
        The status of the update operation performed on the team member.
    """

    client = get_salesforce_client()

    payload: dict[str, Any] = {"TeamRoleId": case_team_member_role_id}

    status_code = client.salesforce_object.CaseTeamMember.update(case_team_member_id, data=payload)  # type: ignore[operator]

    return status_code
