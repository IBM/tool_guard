from datetime import datetime, timedelta
from enum import StrEnum
import json
import re
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class RecurrenceType(StrEnum):
    """Represents the recurrence type for Outlook calendar events."""

    Daily = "daily"
    Weekly = "weekly"
    Monthly = "absoluteMonthly"


@dataclass
class CreateOutlookEventResponse:
    """Represents the result of creating an Outlook event."""

    event_id: str


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def create_outlook_event(
    subject: str,
    content: str,
    start_date_time: str,
    duration: str,
    attendees: str,
    is_online_event: bool,
    location: str,
    recurrence_type: Optional[str] = None,
    frequency: Optional[int] = None,
    days_of_the_week: Optional[str] = None,
    day_of_the_month: Optional[int] = None,
    recurrence_end_date: Optional[str] = None,
) -> CreateOutlookEventResponse:
    """
    Creates an Outlook event.

    Args:
        subject: The subject of the event.
        content: The content/body of the event.
        start_date_time: The start date and time of the event, in format like '2019-03-15T12:00:00 PST'.
        duration: The duration of the event in minutes.
        attendees: A comma-separated list of attendee email addresses.
        is_online_event: Boolean indicating whether the event is an online meeting.
        location: The location where the event will take place.
        recurrence_type: Required if recurrence is needed; valid values are "Daily", "Weekly", or "Monthly".
        frequency: Required if recurrence_type is set; defines how often the event repeats (e.g., every 1 day/week/month).
        days_of_the_week: Required if recurrence_type is "Weekly"; a comma-separated list of weekdays (e.g., "Monday, Friday").
        day_of_the_month: Required if recurrence_type is "Monthly"; the calendar day the event occurs on (e.g., 15).
        recurrence_end_date: Required if recurrence_type is set; the end date for the recurring event in ISO 8601 format (e.g., "2025-07-03").

    Returns:
        ID of the created event.
    """

    client = get_microsoft_client()

    # Extract timezone and clean datetime
    timezone_match = re.search(r"\s([A-Z]{3,4})$", start_date_time)
    timezone = timezone_match.group(1) if timezone_match else "UTC"
    clean_start_date = re.sub(r"\s[A-Z]{3,4}$", "", start_date_time)

    start_datetime = datetime.fromisoformat(clean_start_date.replace("Z", "+00:00"))
    end_datetime = start_datetime + timedelta(minutes=int(duration))
    end_date = end_datetime.isoformat().replace("+00:00", "Z")

    # Build attendees list
    if attendees:
        attendee_list = [
            {"emailAddress": {"address": email.strip()}, "type": "required"}
            for email in attendees.split(",")
            if email.strip()
        ]
    else:
        attendee_list = []

    # Days of the week
    if days_of_the_week:
        try:
            days = (
                json.loads(days_of_the_week)
                if isinstance(days_of_the_week, str)
                else days_of_the_week
            )
        except json.JSONDecodeError:
            days = days_of_the_week.split(",")
        days_of_week_list = [day.strip().capitalize() for day in days if day.strip()]
    else:
        days_of_week_list = []

    payload = {
        "subject": subject,
        "body": {"content": content, "contentType": "HTML"},
        "start": {"dateTime": clean_start_date, "timeZone": timezone},
        "end": {"dateTime": end_date, "timeZone": timezone},
        "attendees": attendee_list,
        "isOnlineMeeting": is_online_event,
        "location": {"displayName": location},
    }

    # Check if the recurrence type is valid and get its value
    recurrence_types = [rec_type.name for rec_type in RecurrenceType]
    if recurrence_type and recurrence_type.capitalize() not in recurrence_types:
        raise ValueError(
            f"Recurrence type '{recurrence_type}' is not a valid value. Accepted values are {recurrence_types}"
        )

    recurrence_value = (
        RecurrenceType[recurrence_type.capitalize()].value if recurrence_type else None
    )

    # Recurrence payload (only if recurrence_type is provided)
    if recurrence_type:
        if not recurrence_end_date:
            raise ValueError(
                "recurrence_end_date must be provided when recurrence_type is specified."
            )

        # Build the recurrence pattern
        pattern = {
            "type": recurrence_value,
            "interval": frequency,
            "daysOfWeek": days_of_week_list if days_of_week_list else None,
            "dayOfMonth": day_of_the_month if day_of_the_month else None,
        }

        # Remove any keys with None values
        pattern = {key: value for key, value in pattern.items() if value is not None}

        recurrence_payload = {
            "pattern": pattern,
            "range": {
                "type": "endDate",
                "startDate": start_datetime.strftime("%Y-%m-%d"),
                "endDate": recurrence_end_date,
            },
        }

        payload["recurrence"] = recurrence_payload

    response = client.post_request(
        endpoint=f"{client.get_user_resource_path()}/events", data=payload
    )
    return CreateOutlookEventResponse(event_id=response["id"])
