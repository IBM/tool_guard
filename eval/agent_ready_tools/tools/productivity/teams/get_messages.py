from http import HTTPStatus
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class MessageBody:
    """Represents the message body in MS Teams."""

    content_type: Optional[str] = None
    content: Optional[str] = None


@dataclass
class Message:
    """Represents the message in MS Teams."""

    id: str
    subject: Optional[str] = None
    web_url: Optional[str] = None
    body: Optional[MessageBody] = None


@dataclass
class MessagesResponse:
    """Represents the result of getting messages in MS Teams."""

    messages: Optional[List[Message]] = None
    http_code: Optional[int] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_messages(team_id: str, channel_id: str) -> MessagesResponse:
    """
    Get messages for given channel in Teams.

    Args:
        team_id: The team_id of the team within the MS Graph API, returned by the `get_teams` tool.
        channel_id: The channel_id of the channel within the MS Graph API, returned by the
            `get_channels` tool.

    Returns:
        List of messages.
    """
    client = get_microsoft_client()

    endpoint = f"/teams/{team_id}/channels/{channel_id}/messages"

    try:
        response = client.get_request(endpoint)

        messages = [
            Message(
                id=message.get("id", ""),
                subject=message.get("subject", ""),
                web_url=message.get("webUrl", ""),
                body=MessageBody(
                    content_type=message.get("body", {}).get("contentType", ""),
                    content=message.get("body", {}).get("content", ""),
                ),
            )
            for message in response.get("value", [])
        ]

        return MessagesResponse(messages=messages)

    except HTTPError as e:
        error_response = e.response.json()
        return MessagesResponse(
            http_code=e.response.status_code,
            error_code=error_response.get("error", {}).get("code", ""),
            error_message=error_response.get("error", {}).get("message", ""),
        )

    except Exception as e:  # pylint: disable=broad-except
        return MessagesResponse(
            http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            error_code="Exception",
            error_message=str(e),
        )
