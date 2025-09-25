from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class CreateTeamResponse:
    """Represents the result of creating a team in Microsoft Teams."""

    http_code: int


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def create_a_team(
    team_name: str, first_channel_name: str, description: Optional[str] = None
) -> CreateTeamResponse:
    """
    Creates a team in Microsoft Teams.

    Args:
        team_name: The name of the team in Microsoft Teams.
        first_channel_name: The name of the first channel in the team in Microsoft Teams.
        description: The description of the team in Microsoft Teams.

    Returns:
        The result of performing the creation of team in Microsoft Teams.
    """
    client = get_microsoft_client()
    # Since there is no API available to fetch the templates and this parameter is mandatory, it is hardcoded to 'standard' and passed within template_name.
    template_name = "https://graph.microsoft.com/v1.0/teamsTemplates('standard')"
    payload: dict[str, Any] = {
        "template@odata.bind": template_name,
        "displayName": team_name,
        "description": description,
        "firstChannelName": first_channel_name,
    }
    response = client.post_request(endpoint="teams", data=payload)
    return CreateTeamResponse(http_code=response["status_code"])
