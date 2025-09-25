import html
import re
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class ChatMessage:
    """Represents a message in a Microsoft Teams chat."""

    chat_message_id: str
    chat_id: str
    message_type: str
    message: str
    web_url: Optional[str] = None


@dataclass
class ChatMessagesResponse:
    """Response containing a list of messages from a Microsoft Teams chat."""

    messages: List[ChatMessage]
    limit: Optional[int] = 0
    skip_token: Optional[str] = None


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_chat_messages(
    chat_id: str, limit: Optional[int] = 10, skip_token: Optional[str] = None
) -> ChatMessagesResponse:
    """
    Retrieves chat messages from a Microsoft Teams chat.

    Args:
        chat_id: The chat_id uniquely identifying them within the MS Graph API, returned by
            `get_chats` tool.
        limit: The maximum number of messages to retrieve in a single API call.
        skip_token: A token used to skip a specific number of items for pagination purposes. Use
            this to retrieve subsequent pages of results when handling large datasets.

    Returns:
        List of chat messages from Microsoft Teams, along with pagination parameters (limit and
        skip_token).
    """
    client = get_microsoft_client()
    endpoint = f"chats/{chat_id}/messages"

    params = {"$top": limit, "$skiptoken": skip_token}

    params = {key: value for key, value in params.items() if value}

    response = client.get_request(endpoint=endpoint, params=params)

    messages: List[ChatMessage] = []

    # Extract limit and skip_token from @odata.nextLink if it exists
    next_api_link = response.get("@odata.nextLink", "")
    if next_api_link:
        query_params = get_query_param_from_links(href=next_api_link)
        output_limit = query_params.get("$top", "")
        output_skip_token = query_params.get("$skiptoken", "")
    else:
        output_limit = limit
        output_skip_token = skip_token

    for item in response["value"]:

        content = item.get("body", {}).get("content", "")
        plain_text = ""
        if content:
            # Remove HTML tags
            text = re.sub(r"<[^>]+>", "", content)

            # Unescape HTML entities like &nbsp;
            plain_text = html.unescape(text)

        messages.append(
            ChatMessage(
                chat_message_id=item.get("id", ""),
                chat_id=item.get("chatId", ""),
                message_type=item.get("messageType", ""),
                message=plain_text,
                web_url=item.get("webUrl", ""),
            )
        )

    return ChatMessagesResponse(
        messages=messages,
        limit=int(output_limit),
        skip_token=output_skip_token,
    )
