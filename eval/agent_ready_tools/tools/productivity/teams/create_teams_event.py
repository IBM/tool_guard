from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class Attendee:
    """Represents an attendee of a Teams event."""

    name: str
    email: str


@dataclass
class EventTime:
    """Represents event time information."""

    date_time: str
    time_zone: str


@dataclass
class EventLocation:
    """Represents event location information."""

    display_name: str


@dataclass
class EventOrganizer:
    """Represents the organizer of the event."""

    name: str
    email: str


@dataclass
class CreateTeamsEventResponse:
    """Represents the result of creating a Teams event."""

    event_id: str
    created_date_time: str
    subject: str
    body: Optional[str]
    start: EventTime
    end: EventTime
    location: EventLocation
    attendees: List[Attendee]
    organizer: EventOrganizer
    http_code: int


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def create_teams_event(
    subject: str,
    content: str,
    start_date_time: str,
    end_date_time: str,
    time_zone: str,
    location: str,
    attendees: str,
) -> CreateTeamsEventResponse:
    """
    Creates a Microsoft Teams event.

    Args:
        subject: The subject of the event.
        content: The content or body text of the event.
        start_date_time: The start date and time of the event in ISO format (e.g.,'2023-04-15T12:00:00').
        end_date_time: The end date and time of the event in ISO format (e.g.,'2023-04-15T13:00:00').
        time_zone: The time zone for the event (e.g., 'UTC', 'Pacific Standard Time').
        location: The location of the event.
        attendees: List of attendee objects, each containing 'name' and 'email' keys.

    Returns:
        Details of the created event.
    """

    client = get_microsoft_client()

    attendee_list = []
    email_list = []
    if isinstance(attendees, str):
        # Handle comma-separated string or single email
        email_list = [email.strip() for email in attendees.split(",")]

    for email in email_list:
        if isinstance(email, str) and email:
            name = extract_name_from_email(email)
            attendee_list.append(
                {"emailAddress": {"address": email, "name": name}, "type": "required"}
            )

    payload = {
        "subject": subject,
        "body": {"content": content},
        "start": {"dateTime": start_date_time, "timeZone": time_zone},
        "end": {"dateTime": end_date_time, "timeZone": time_zone},
        "location": {"displayName": location},
        "attendees": attendee_list,
    }

    response = client.post_request(
        endpoint=f"{client.get_user_resource_path()}/calendar/events", data=payload
    )

    attendees_result = []
    for attendee in response.get("attendees", []):
        email_address: dict = attendee.get("emailAddress", {})  # type: ignore
        attendees_result.append(
            Attendee(name=email_address.get("name", ""), email=email_address.get("address", ""))
        )

    organizer_data = response.get("organizer", {}).get("emailAddress", {})
    http_code = response.get("status_code", 200)

    return CreateTeamsEventResponse(
        event_id=response.get("id", ""),
        created_date_time=response.get("createdDateTime", ""),
        subject=response.get("subject", ""),
        body=response.get("body", {}).get("content", ""),
        start=EventTime(
            date_time=response.get("start", {}).get("dateTime", ""),
            time_zone=response.get("start", {}).get("timeZone", ""),
        ),
        end=EventTime(
            date_time=response.get("end", {}).get("dateTime", ""),
            time_zone=response.get("end", {}).get("timeZone", ""),
        ),
        location=EventLocation(display_name=response.get("location", {}).get("displayName", "")),
        attendees=attendees_result,
        organizer=EventOrganizer(
            name=organizer_data.get("name", ""), email=organizer_data.get("address", "")
        ),
        http_code=http_code,
    )


def extract_name_from_email(email: str) -> str:
    """
    Args:
        email: The email which is to extract name.

    Returns:
        The name extracted from email.
    """
    email_name = email.split("@")[0]
    name_value = email_name.replace(".", " ").replace("_", " ").split()
    return " ".join(name.capitalize() for name in name_value)
