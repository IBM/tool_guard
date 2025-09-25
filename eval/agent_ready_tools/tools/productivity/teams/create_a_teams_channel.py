import http
from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
import requests

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class CreateChannelResponse:
    """Represents the result of creating a teams channel in MS Teams."""

    channel_name: str
    http_code: int
    error_message: Optional[str]


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def create_a_teams_channel(
    team_id: str, channel_name: str, description: str
) -> CreateChannelResponse:
    """
    Creates a teams channel in Microsoft Teams.

    Args:
        team_id: The team_id of the team in Microsoft Teams returned by the `get_teams` tool.
        channel_name: The display name of the channel in Teams.
        description: The description of the channel in Teams.

    Returns:
        The result of performing the creation of teams channel.
    """
    try:
        client = get_microsoft_client()

        payload: dict[str, Any] = {"displayName": channel_name, "description": description}

        response = client.post_request(endpoint=f"teams/{team_id}/channels", data=payload)

        return CreateChannelResponse(
            channel_name=response.get("displayName", ""),
            error_message=None,
            http_code=int(response.get("status_code", 200)),
        )

    except requests.exceptions.HTTPError as err:
        if err.response.status_code == http.HTTPStatus.BAD_REQUEST:
            error_detail = err.response.json()
            error_message = error_detail.get("error", {}).get("message", "").lower()
            return CreateChannelResponse(
                channel_name="", error_message=error_message, http_code=err.response.status_code
            )

        else:
            return CreateChannelResponse(
                channel_name="",
                error_message=f"Unexpected error",
                http_code=err.response.status_code,
            )
