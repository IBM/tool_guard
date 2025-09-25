from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class TeamMembers:
    """Represents the team members in Microsoft Teams."""

    display_name: str
    email: str
    user_id: str


@dataclass
class TeamMembersResponse:
    """A list of team members in Microsoft Teams."""

    team_members: List[TeamMembers]


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_team_members(team_id: str) -> TeamMembersResponse:
    """
    Gets a list of team members in the Microsoft Teams.

    Args:
        team_id: The team_id of the team, returned by the `get_teams` tool.

    Returns:
        A list of team members from Microsoft Teams.
    """

    client = get_microsoft_client()
    response = client.get_request(endpoint=f"teams/{team_id}/members")

    team_members = [
        TeamMembers(
            display_name=result.get("displayName", ""),
            email=result.get("email", ""),
            user_id=result.get("userId", ""),
        )
        for result in response.get("value", [])
    ]
    return TeamMembersResponse(team_members=team_members)
