from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class Event:
    """Represents the result of an event in Outlook."""

    id: str
    subject: str
    start_time: str
    end_time: str


@dataclass
class GetAllEventsResponse:
    """Represents the result of an event delete operation in Outlook."""

    events: list[Event]


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_all_events(
    event_subject: Optional[str] = None,
    start_date_time: Optional[str] = None,
    end_date_time: Optional[str] = None,
) -> GetAllEventsResponse:
    """
    Get all events from calendar in Outlook.

    Args:
        event_subject: The subject of the event to filter.
        start_date_time: The starting date time of an event in ISO 8601 format (e.g., YYYY-MM-DDTHH:mm:ss.sss).
        end_date_time: The ending date time of an event in ISO 8601 format (e.g., YYYY-MM-DDTHH:mm:ss.sss).

    Returns:
        List of events.
    """
    client = get_microsoft_client()
    endpoint = f"{client.get_user_resource_path()}/events?$select=subject,start,end"

    params: Dict[str, Any] = {}

    filters = []

    if event_subject:
        filters.append(f"subject eq '{event_subject}'")
    if start_date_time:
        filters.append(f"start/dateTime ge '{start_date_time}'")
    if end_date_time:
        filters.append(f"end/dateTime le '{end_date_time}'")

    if filters:
        params["$filter"] = " and ".join(filters)

    response = client.get_request(endpoint=endpoint, params=params)

    events: list[Event] = []

    for result in response["value"]:
        events.append(
            Event(
                id=result.get("id", ""),
                subject=result.get("subject", ""),
                start_time=result.get("start", {}).get("dateTime", ""),
                end_time=result.get("end", {}).get("dateTime", ""),
            )
        )

    return GetAllEventsResponse(events=events)
