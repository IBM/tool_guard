from typing import Any

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class SendChatMessageResponse:
    """Represents the result of sending a message to a chat in Microsoft Teams."""

    message: str


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def send_a_chat_message(chat_id: str, message: str) -> SendChatMessageResponse:
    """
    Sends a chat message in Microsoft Teams.

    Args:
        chat_id: The chat_id of the chat in Microsoft Teams returned by the `get_chats` tool.
        message: The message to be sent in Teams chat.

    Returns:
        The result of sending a chat message.
    """
    client = get_microsoft_client()

    payload: dict[str, Any] = {"body": {"content": message}}

    response = client.post_request(endpoint=f"chats/{chat_id}/messages", data=payload)

    return SendChatMessageResponse(message=response.get("body", "{}").get("content", ""))
