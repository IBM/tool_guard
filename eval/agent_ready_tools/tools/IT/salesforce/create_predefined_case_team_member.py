from typing import Any

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@dataclass
class CreatePredefinedCaseTeamMemberResponse:
    """Represents the result of creating a predefined case team member in Salesforce."""

    predefined_case_team_member_id: str


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def create_predefined_case_team_member(
    member_id: str,
    case_team_member_role_id: str,
    team_template_id: str,
) -> CreatePredefinedCaseTeamMemberResponse:
    """
    Creates a predefined case team member in Salesforce.

    Args:
        member_id: The id of the member, returned by the `list_case_team_members` tool in
            Salesforce.
        case_team_member_role_id: The id of the team role, returned by the
            `list_case_team_member_roles` tool in Salesforce.
        team_template_id: The id of the team template, returned by the `get_predefined_case_teams`
            tool in Salesforce.

    Returns:
        The result of creating a predefined case team member.
    """

    client = get_salesforce_client()

    payload: dict[str, Any] = {
        "MemberId": member_id,
        "TeamRoleId": case_team_member_role_id,
        "TeamTemplateId": team_template_id,
    }

    response = client.salesforce_object.CaseTeamTemplateMember.create(data=payload)  # type: ignore[operator]

    return CreatePredefinedCaseTeamMemberResponse(
        predefined_case_team_member_id=response.get("id", "")
    )
