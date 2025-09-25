from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.slack_client import get_slack_client
from agent_ready_tools.utils.tool_credentials import SLACK_CONNECTIONS


@dataclass
class SendMessageResponse:
    """Represents the result of sending a message in Slack."""

    send_message_status: bool


@tool(expected_credentials=SLACK_CONNECTIONS)
def send_a_slack_message(
    channel_id: str,
    text: Optional[str] = None,
    attachments: Optional[Any] = None,
    blocks: Optional[Any] = None,
) -> SendMessageResponse:
    """
    Sends a message to a channel in Slack.

    Args:
        channel_id: The id of the channel to which the message has to be sent.
        text: The content of the message.
        attachments: The attachments to be sent in the message.
        blocks: Used to define the layout and components of a message.

    Returns:
        Confirmation that the message was sent.
    """

    client = get_slack_client()

    payload = {
        "channel": channel_id,
        "text": text,
        "attachments": attachments,
        "blocks": blocks,
    }

    payload = {key: value for key, value in payload.items() if value}

    response = client.post_request(entity="chat.postMessage", payload=payload)
    return SendMessageResponse(
        send_message_status=response.get("ok", ""),
    )
