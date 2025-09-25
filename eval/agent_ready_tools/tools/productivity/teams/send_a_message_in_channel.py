from http import HTTPStatus
from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class SendMessageChannelResponse:
    """Represents the result of sending a message in Microsoft Teams channel."""

    message: Optional[str] = None
    http_code: Optional[int] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def send_a_message_in_channel(
    team_id: str, channel_id: str, message: str
) -> SendMessageChannelResponse:
    """
    Sends a message to a channel in Microsoft Teams.

    Args:
        team_id: The team_id of the team in Microsoft Teams returned by the `get_teams` tool.
        channel_id: The channel_id of the channel in Microsoft Teams returned by the `get_channels`
            tool.
        message: The message to be sent in a Microsoft Teams channel.

    Returns:
        Confirmation that the message was sent.
    """
    client = get_microsoft_client()
    payload: dict[str, Any] = {"body": {"content": message}}

    try:
        response = client.post_request(
            endpoint=f"teams/{team_id}/channels/{channel_id}/messages", data=payload
        )

        return SendMessageChannelResponse(message=response.get("body", {}).get("content", ""))

    except HTTPError as e:
        error_response = e.response.json()
        return SendMessageChannelResponse(
            http_code=e.response.status_code,
            error_code=error_response.get("error", {}).get("code", ""),
            error_message=error_response.get("error", {}).get("message", ""),
        )

    except Exception as e:  # pylint: disable=broad-except
        return SendMessageChannelResponse(
            http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            error_code="Exception",
            error_message=str(e),
        )
