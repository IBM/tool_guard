from http import HTTPStatus
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class GetChannels:
    """Represents a Microsoft channel in Microsoft Teams."""

    channel_id: str
    display_name: str
    web_url: str
    description: Optional[str] = None
    email: Optional[str] = None


@dataclass
class GetChannelsResponse:
    """Represents the result of getting all channels in Microsoft Teams."""

    channels: Optional[List[GetChannels]] = None
    http_code: Optional[int] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_channels(team_id: str) -> GetChannelsResponse:
    """
    Retrieves all channels in Microsoft Teams for a given team.

    Args:
        team_id: The team_id uniquely identifying them within Microsoft Teams, is returned by the
            `get_teams` tool.

    Returns:
        List of channels.
    """
    client = get_microsoft_client()

    endpoint = f"teams/{team_id}/allChannels"

    try:
        response = client.get_request(endpoint=endpoint)
        channels: List[GetChannels] = []

        for result in response.get("value", []):
            channels.append(
                GetChannels(
                    channel_id=result.get("id", ""),
                    display_name=result.get("displayName", ""),
                    description=result.get("description", ""),
                    email=result.get("email", ""),
                    web_url=result.get("webUrl", ""),
                )
            )

        return GetChannelsResponse(channels=channels)

    except HTTPError as e:
        error_response = e.response.json()
        return GetChannelsResponse(
            http_code=e.response.status_code,
            error_code=error_response.get("error", {}).get("code", ""),
            error_message=error_response.get("error", {}).get("message", ""),
        )

    except Exception as e:  # pylint: disable=broad-except
        return GetChannelsResponse(
            http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            error_code="Exception",
            error_message=str(e),
        )
