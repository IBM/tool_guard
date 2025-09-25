from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.teams.get_events import get_events


def test_get_events_with_mock() -> None:
    """Verifies that the `get_events` tool can successfully return a list of events from a Microsoft
    Teams calendar."""

    # Mock input parameters
    limit = 20
    skip = 0

    # Mock test data
    test_data = {
        "subject": "project planning",
        "owner_name": "Test User",
        "event_link": "https://teams.microsoft.com/l/meetup-join/...",
        "start_date_time": "2025-04-07T02:00:00.0002605",
        "start_timezone": "Central Standard Time",
        "original_start_timezone": "UTC",
        "end_date_time": "2025-04-07T02:30:00.0002605",
        "end_timezone": "Central Standard Time",
        "original_end_timezone": "UTC",
        "event_id": "AAMkADYyODVkMjM5...",
        "attendees": ["test1@microsoft.com", "test2@microsoft.com"],
        "user_name": "user@example.com",
    }

    with patch(
        "agent_ready_tools.tools.productivity.teams.get_events.get_microsoft_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {
                    "subject": test_data["subject"],
                    "organizer": {
                        "emailAddress": {
                            "name": test_data["owner_name"],
                        }
                    },
                    "onlineMeeting": {"joinUrl": test_data["event_link"]},
                    "start": {
                        "dateTime": test_data["start_date_time"],
                        "timeZone": test_data["original_start_timezone"],
                    },
                    "end": {
                        "dateTime": test_data["end_date_time"],
                        "timeZone": test_data["original_end_timezone"],
                    },
                    "originalStartTimeZone": test_data["start_timezone"],
                    "originalEndTimeZone": test_data["end_timezone"],
                    "id": test_data["event_id"],
                    "attendees": [
                        {"emailAddress": {"address": "test1@microsoft.com"}},
                        {"emailAddress": {"address": "test2@microsoft.com"}},
                    ],
                }
            ]
        }
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        # Call the function
        response = get_events(limit=limit, skip=skip)

        # Verify the response
        event = response.events[0]
        assert event.subject == test_data["subject"]
        assert event.owner_name == test_data["owner_name"]
        assert event.event_link == test_data["event_link"]
        assert event.start_date_time == test_data["start_date_time"]
        assert event.attendees == test_data["attendees"]
        assert event.event_id == test_data["event_id"]
        assert event.start_timezone == test_data["start_timezone"]
        assert event.original_start_timezone == test_data["original_start_timezone"]
        assert event.end_date_time == test_data["end_date_time"]
        assert event.end_timezone == test_data["end_timezone"]
        assert event.original_end_timezone == test_data["original_end_timezone"]

        # Verify API call
        mock_client.get_request.assert_called_once_with(
            endpoint=f"users/{test_data["user_name"]}/calendar/events",
            params={"$top": limit, "$skip": skip},
        )


def test_get_events_with_filter() -> None:
    """Verifies that the `get_events` tool can successfully return a list of events from a Microsoft
    Teams calendar."""

    # Mock input parameters
    limit = 20
    skip = 0

    # Mock test data
    test_data = {
        "subject": "project planning",
        "owner_name": "Test User",
        "event_link": "https://teams.microsoft.com/l/meetup-join/...",
        "start_date_time": "2025-04-07T02:00:00.0002605",
        "start_timezone": "Central Standard Time",
        "original_start_timezone": "UTC",
        "end_date_time": "2025-04-07T02:30:00.0002605",
        "end_timezone": "Central Standard Time",
        "original_end_timezone": "UTC",
        "event_id": "AAMkADYyODVkMjM5...",
        "attendees": ["test1@microsoft.com", "test2@microsoft.com"],
        "user_name": "user@example.com",
    }

    with patch(
        "agent_ready_tools.tools.productivity.teams.get_events.get_microsoft_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {
                    "subject": test_data["subject"],
                    "organizer": {
                        "emailAddress": {
                            "name": test_data["owner_name"],
                        }
                    },
                    "onlineMeeting": {"joinUrl": test_data["event_link"]},
                    "start": {
                        "dateTime": test_data["start_date_time"],
                        "timeZone": test_data["original_start_timezone"],
                    },
                    "end": {
                        "dateTime": test_data["end_date_time"],
                        "timeZone": test_data["original_end_timezone"],
                    },
                    "originalStartTimeZone": test_data["start_timezone"],
                    "originalEndTimeZone": test_data["end_timezone"],
                    "id": test_data["event_id"],
                    "attendees": [
                        {"emailAddress": {"address": "test1@microsoft.com"}},
                        {"emailAddress": {"address": "test2@microsoft.com"}},
                    ],
                }
            ]
        }
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        # Call the function
        response = get_events(
            start_date_time=test_data["start_date_time"],
            end_date_time=test_data["end_date_time"],
            limit=limit,
            skip=skip,
        )

        # Verify the response
        event = response.events[0]
        assert event.subject == test_data["subject"]
        assert event.owner_name == test_data["owner_name"]
        assert event.event_link == test_data["event_link"]
        assert event.start_date_time == test_data["start_date_time"]
        assert event.attendees == test_data["attendees"]
        assert event.event_id == test_data["event_id"]
        assert event.start_timezone == test_data["start_timezone"]
        assert event.original_start_timezone == test_data["original_start_timezone"]
        assert event.end_date_time == test_data["end_date_time"]
        assert event.end_timezone == test_data["end_timezone"]
        assert event.original_end_timezone == test_data["original_end_timezone"]

        # Verify API call
        mock_client.get_request.assert_called_once_with(
            endpoint=f"users/{test_data["user_name"]}/calendar/events",
            params={
                "$top": limit,
                "$skip": skip,
                "$filter": f"start/dateTime ge '{test_data["start_date_time"]}' and end/dateTime le '{test_data['end_date_time']}'",
            },
        )
