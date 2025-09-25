from typing import Union

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def update_predefined_case_team_member(
    case_team_member_id: str,
    team_role_id: str,
) -> Union[int, str]:
    """
    Updates an existing predefined case team member in Salesforce.

    Args:
        case_team_member_id: The id of the predefined case team member in Salesforce returned by the
            tool `get_predefined_case_team_members`.
        team_role_id: The role id of the predefined case team member in Salesforce returned by the
            tool `list_case_team_member_roles`.

    Returns:
        The status of the update operation performed on the predefined case team member.
    """

    client = get_salesforce_client()

    data = {"TeamRoleId": team_role_id}

    try:
        status_code = client.salesforce_object.CaseTeamTemplateMember.update(
            case_team_member_id, data
        )  # type: ignore[operator]
        return status_code

    except Exception as e:  # pylint: disable=broad-exception-caught
        # Log the error or return it for debugging
        return f"Failed to update case team member: {str(e)}"
