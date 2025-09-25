from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class CreateCalendarGroupResponse:
    """Represents the result of creating a calendar group."""

    http_code: Optional[int] = None
    group_id: Optional[str] = None


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def create_calendar_group(name: str) -> CreateCalendarGroupResponse:
    """
    Creates a calendar group in Outlook.

    Args:
        name: The name of the calendar group.

    Returns:
        HTTP status code and ID of created calendar group
    """
    client = get_microsoft_client()

    payload = {
        "name": name,
    }
    response = client.post_request(
        endpoint=f"{client.get_user_resource_path()}/calendarGroups", data=payload
    )
    return CreateCalendarGroupResponse(
        http_code=response.get("status_code", None), group_id=response.get("id", None)
    )
