from typing import Any, List, Optional, Tuple

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class Chats:
    """Represents the details of a chat in Microsoft Teams."""

    chat_id: str
    chat_type: str
    member_details: List[Tuple[Any, Any]]
    chat_name: Optional[str] = None


@dataclass
class ChatsResponse:
    """Represents a list of chats in Microsoft Teams."""

    chats: List[Chats]
    limit: Optional[int] = 0
    skip_token: Optional[str] = None


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_chats(
    chat_name: Optional[str] = None, limit: Optional[int] = 50, skip_token: Optional[str] = None
) -> ChatsResponse:
    """
    Retrieves a list of chats in Microsoft Teams.

    Args:
        chat_name: The chat_name is used to filter results in Microsoft Teams based upon the topic
            of the chat.
        limit: The maximum number of chats retrieved in a single API call. Defaults to 50. Use this
            to control the size of the result set in Microsoft Teams.
        skip_token: A token used to skip a specific number of items for pagination purposes. Use
            this to retrieve subsequent pages of results when handling large datasets.

    Returns:
        List of all the chats in Microsoft Teams, along with pagination parameters (limit and skip).
    """

    client = get_microsoft_client()
    params = {
        "$top": limit,
        "$skiptoken": skip_token,
        "$expand": "members",
        "$filter": f"startswith(topic,'{chat_name}')" if chat_name else None,
    }
    params = {key: value for key, value in params.items() if value}

    response = client.get_request(
        endpoint=f"{client.get_user_resource_path()}/chats", params=params
    )

    # Extract limit and skiptoken from @odata.nextLink if it exists
    output_limit = None
    output_skiptoken = None
    next_api_link = response.get("@odata.nextLink", "")
    if next_api_link:
        query_params = get_query_param_from_links(href=next_api_link)
        output_limit = int(query_params.get("$top", ""))
        output_skiptoken = query_params.get("$skiptoken", "")

    chats_list: List[Chats] = []

    for chat in response["value"]:
        chats_list.append(
            Chats(
                chat_id=chat.get("id", ""),
                chat_name=chat.get("topic", ""),
                chat_type=chat.get("chatType", ""),
                member_details=[
                    (member.get("displayName"), member.get("email"))
                    for member in chat.get("members", [])
                ],
            )
        )

    return ChatsResponse(chats=chats_list, limit=output_limit, skip_token=output_skiptoken)
