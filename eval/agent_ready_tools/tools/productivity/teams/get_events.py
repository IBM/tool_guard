from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class TeamsEvent:
    """Represents an event in Microsoft Teams."""

    subject: str
    owner_name: str
    start_date_time: str
    end_date_time: str
    attendees: List[str]
    event_id: str
    start_timezone: str
    end_timezone: str
    original_start_timezone: str
    original_end_timezone: str
    event_link: Optional[str] = None


@dataclass
class EventsResponse:
    """Represents the response for retrieving events."""

    events: List[TeamsEvent]
    limit: Optional[int]
    skip: Optional[int]


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_events(
    event_subject: Optional[str] = None,
    start_date_time: Optional[str] = None,
    end_date_time: Optional[str] = None,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> EventsResponse:
    """
    Retrieves events from a Microsoft Teams calendar.

    Args:
        event_subject: The subject of the event to filter.
        start_date_time: The starting date time of an event in ISO 8601 format (e.g., YYYY-MM-DDTHH:mm:ss.sss).
        end_date_time: The ending date time of an event in ISO 8601 format (e.g., YYYY-MM-DDTHH:mm:ss.sss).
        limit: The maximum number of events to retrieve in a single API call. Defaults to 20. Use
            this to control the size of the result set.
        skip: The number of events to skip for pagination purposes. Use this to retrieve subsequent
            pages of results when handling large datasets.

    Returns:
        The list of events.
    """
    client = get_microsoft_client()

    params: Dict[str, Any] = {}

    if event_subject:
        if start_date_time:
            if end_date_time:
                params["$filter"] = (
                    f"subject eq '{event_subject}' and start/dateTime ge '{start_date_time}' and end/dateTime le '{end_date_time}'"
                )
            else:
                params["$filter"] = (
                    f"subject eq '{event_subject}' and start/dateTime ge '{start_date_time}'"
                )
        elif end_date_time:
            params["$filter"] = (
                f"subject eq '{event_subject}' and end/dateTime le '{end_date_time}'"
            )
        else:
            params["$filter"] = f"subject eq '{event_subject}'"
    elif start_date_time:
        if end_date_time:
            params["$filter"] = (
                f"start/dateTime ge '{start_date_time}' and end/dateTime le '{end_date_time}'"
            )
        else:
            params["$filter"] = f"start/dateTime ge '{start_date_time}'"
    elif end_date_time:
        params["$filter"] = f"end/dateTime le '{end_date_time}'"
    if limit:
        params["$top"] = limit
    if skip is not None:
        params["$skip"] = skip
    endpoint = f"{client.get_user_resource_path()}/calendar/events"

    response = client.get_request(endpoint=endpoint, params=params)

    events = [
        TeamsEvent(
            subject=event.get("subject", ""),
            owner_name=event.get("organizer", {}).get("emailAddress", {}).get("name", ""),
            event_link=(
                event.get("onlineMeeting", {}).get("joinUrl") if event.get("onlineMeeting") else ""
            ),
            start_date_time=event.get("start", {}).get("dateTime", ""),
            start_timezone=event.get("originalStartTimeZone", ""),
            attendees=[
                attendee.get("emailAddress", {}).get("address")
                for attendee in event.get("attendees", [])
            ],
            event_id=event.get("id", ""),
            original_start_timezone=event.get("start", {}).get("timeZone", ""),
            end_date_time=event.get("end", {}).get("dateTime", ""),
            end_timezone=event.get("originalEndTimeZone", ""),
            original_end_timezone=event.get("end", {}).get("timeZone", ""),
        )
        for event in response.get("value", [])
    ]

    # Extract limit and skip from @odata.nextLink if it exists
    output_limit = None
    output_skip = None
    next_api_link = response.get("@odata.nextLink", "")
    if next_api_link:
        query_params = get_query_param_from_links(next_api_link)
        output_limit = int(query_params["$top"])
        output_skip = int(query_params["$skip"])

    return EventsResponse(
        events=events,
        limit=output_limit,
        skip=output_skip,
    )
