from typing import Any

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@dataclass
class CreateCaseTeamMemberResponse:
    """Represents the response of creating a case team member in Salesforce."""

    record_id: str


@tool(permission=ToolPermission.WRITE_ONLY, expected_credentials=SALESFORCE_CONNECTIONS)
def create_case_team_member(
    case_id: str, user_id: str, case_team_member_role_id: str
) -> CreateCaseTeamMemberResponse:
    """
    Creates a case team member in Salesforce.

    Args:
        case_id: The unique id of the case obtained from `list_cases` tool.
        user_id: The unique user id of the user obtained from `list_users` tool.
        case_team_member_role_id: The unique id of the team role obtained from
            `list_case_team_member_roles` tool.

    Returns:
        Returns the result of the created team member.
    """

    client = get_salesforce_client()

    payload: dict[str, Any] = {
        "ParentId": case_id,
        "MemberId": user_id,
        "TeamRoleId": case_team_member_role_id,
    }

    response = client.salesforce_object.CaseTeamMember.create(data=payload)  # type: ignore[operator]

    return CreateCaseTeamMemberResponse(record_id=response.get("id", ""))
