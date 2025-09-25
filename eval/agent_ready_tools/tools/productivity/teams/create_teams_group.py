from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class CreateTeamsGroupResponse:
    """Represents the HTTP status code result of creating a Teams group in Microsoft Teams."""

    http_code: int


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def create_teams_group(
    display_name: str,
    mail_nickname: str,
    mail_enabled: bool = True,
    security_enabled: bool = False,
) -> CreateTeamsGroupResponse:
    """
    Creates a new Microsoft Teams group.

    Args:
        display_name: The display name of the new Teams group.
        mail_nickname: The mail nickname for the group, used to create the email address.
        mail_enabled: Boolean flag indicating if the group is mail-enabled.
        security_enabled: Boolean flag indicating if the group is a security group.

    Returns:
        HTTP status code of the create Teams group operation.
    """
    client = get_microsoft_client()

    payload = {
        "displayName": display_name,
        "mailNickname": mail_nickname,
        "mailEnabled": mail_enabled,
        "securityEnabled": security_enabled,
        "groupTypes": ["Unified"],
    }

    response = client.post_request(endpoint="groups", data=payload)

    return CreateTeamsGroupResponse(http_code=int(response["status_code"]))
