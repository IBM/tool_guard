from typing import Any

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class UpdateEventResponse:
    """Represents the result of updating an event in Microsoft Teams."""

    event_subject: str
    start_datetime: str
    start_timezone: str
    end_datetime: str
    end_timezone: str


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def update_an_event(
    event_id: str, start_datetime: str, end_datetime: str, timezone: str
) -> UpdateEventResponse:
    """
    Updates the event in the Microsoft Teams.

    Args:
        event_id: The event_id unique identifier of the event in Microsoft Teams, returned by the
            tool `get_events`.
        start_datetime: The start date and time for the period to retrieve the event, in ISO 8601
            format (eg.,YYYY-MM-DDTHHMM).
        end_datetime: The end date and time for the period to retrieve the event, in ISO 8601 format
            (eg.,YYYY-MM-DDTHHMM).
        timezone: The timezone of start and end date time of the event in Microsoft Teams, returned
            by the tool `get_timezones`.

    Returns:
        The result from updating an event.
    """

    client = get_microsoft_client()

    data: dict[str, Any] = {
        "start": {"dateTime": start_datetime, "timeZone": timezone},
        "end": {"dateTime": end_datetime, "timeZone": timezone},
    }

    endpoint = f"{client.get_user_resource_path()}/calendar/events/{event_id}"

    response = client.update_request(endpoint=endpoint, data=data)

    return UpdateEventResponse(
        event_subject=response.get("subject", ""),
        start_datetime=response.get("start", {}).get("dateTime", ""),
        end_datetime=response.get("end", {}).get("dateTime", ""),
        start_timezone=response.get("start", {}).get("timeZone", ""),
        end_timezone=response.get("end", {}).get("timeZone", ""),
    )
