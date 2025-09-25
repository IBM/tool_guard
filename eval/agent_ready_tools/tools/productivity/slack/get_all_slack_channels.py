from typing import Any, Dict, List, Literal, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.slack_client import get_slack_client
from agent_ready_tools.utils.tool_credentials import SLACK_CONNECTIONS


@dataclass
class Channel:
    """Represents the Channel details in Slack."""

    channel_id: str
    channel_name: str
    is_channel: bool
    is_im: bool  # Instant message: refers to a private one-to-one direct message between two users
    is_mpim: bool  # Multi-party instant message: refers to a private group conversation involving multiple users
    is_private: bool
    is_member: bool


@dataclass
class GetallchannelsResponse:
    """Represents the list of Channels in Slack."""

    channels: List[Channel]
    next_cursor: Optional[str]


@tool(expected_credentials=SLACK_CONNECTIONS)
def get_all_slack_channels(
    cursor: Optional[str] = None,
    exclude_archived: Optional[bool] = True,
    limit: Optional[int] = 20,
    team_id: Optional[str] = None,
    types: Literal["public_channel", "private_channel", "mpim", "im"] = "public_channel",
) -> GetallchannelsResponse:
    """
    Returns all channels of mentioned type from Slack.

    Args:
        cursor: used for pagination.
        exclude_archived: excludes archived channels.
        limit: limits the number of channels in response.
        team_id: team_id to list channels.
        types: types of the channels.

    Returns:
        The list of channels.
    """

    types_str = ",".join(map(str, types)) if isinstance(types, list) else str(types)

    client = get_slack_client()

    params: Dict[str, Any] = {}

    params["types"] = types_str
    params["limit"] = limit
    params["exclude_archived"] = exclude_archived
    if cursor:
        params["cursor"] = cursor
    if team_id:
        params["team_id"] = team_id

    response = client.get_request(entity="conversations.list", params=params)

    channels = [
        Channel(
            channel_id=result.get("id", ""),
            channel_name=result.get("name", ""),
            is_channel=result.get("is_channel", ""),
            is_im=result.get("is_im", ""),
            is_mpim=result.get("is_mpim", ""),
            is_private=result.get("is_private", ""),
            is_member=result.get("is_member", ""),
        )
        for result in response.get("channels", [])
    ]

    next_cursor = response.get("response_metadata", {}).get("next_cursor", "")

    return GetallchannelsResponse(channels=channels, next_cursor=next_cursor)
