from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class DeleteEventResponse:
    """Represents the result of an event delete operation in Outlook."""

    http_code: int


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def delete_event(event_id: str) -> DeleteEventResponse:
    """
    Delete a calendar event from Outlook.

    Args:
        event_id: The event_id uniquely identifying them within the MS Graph API, as specified by
            the `get_all_events` tool.

    Returns:
        Http response code.
    """
    client = get_microsoft_client()

    endpoint = f"{client.get_user_resource_path()}/events/{event_id}"
    response = client.delete_request(endpoint)

    return DeleteEventResponse(http_code=response)
