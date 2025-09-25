from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.teams.create_teams_event import create_teams_event


def test_create_teams_event() -> None:
    """Verify that the `create_teams_event` tool can successfully create a Teams event."""

    test_data = {
        "event_id": "ABC123456789",
        "created_date_time": "2025-03-24T11:45:30Z",
        "subject": "Team Meeting",
        "content": "Discussing project updates",
        "start_date_time": "2025-03-24T12:00:00",
        "end_date_time": "2025-03-24T13:00:00",
        "time_zone": "UTC",
        "location": "Conference Room A",
        "attendees": "john.doe@example.com",
        "http_code": 201,
        "user_name": "user@example.com",
    }

    mock_response = {
        "id": test_data["event_id"],
        "createdDateTime": test_data["created_date_time"],
        "subject": test_data["subject"],
        "body": {
            "content": test_data["content"],
        },
        "start": {
            "dateTime": test_data["start_date_time"],
            "timeZone": test_data["time_zone"],
        },
        "end": {
            "dateTime": test_data["end_date_time"],
            "timeZone": test_data["time_zone"],
        },
        "location": {
            "displayName": test_data["location"],
        },
        "attendees": [
            {
                "emailAddress": {
                    "address": "john.doe@example.com",
                    "name": "John Doe",
                },
                "type": "required",
            },
        ],
        "organizer": {
            "emailAddress": {
                "address": "organizer@example.com",
                "name": "Meeting Organizer",
            },
        },
        "status_code": test_data["http_code"],
    }

    with patch(
        "agent_ready_tools.tools.productivity.teams.create_teams_event.get_microsoft_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = mock_response
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        response = create_teams_event(
            subject=test_data["subject"],
            content=test_data["content"],
            start_date_time=test_data["start_date_time"],
            end_date_time=test_data["end_date_time"],
            time_zone=test_data["time_zone"],
            location=test_data["location"],
            attendees=test_data["attendees"],
        )

        assert response
        assert response.event_id == test_data["event_id"]
        assert response.created_date_time == test_data["created_date_time"]
        assert response.subject == test_data["subject"]
        assert response.body == test_data["content"]
        assert response.start.date_time == test_data["start_date_time"]
        assert response.start.time_zone == test_data["time_zone"]
        assert response.end.date_time == test_data["end_date_time"]
        assert response.end.time_zone == test_data["time_zone"]
        assert response.location.display_name == test_data["location"]
        assert response.attendees[0].name == "John Doe"
        assert response.attendees[0].email == "john.doe@example.com"
        assert response.organizer.name == "Meeting Organizer"
        assert response.organizer.email == "organizer@example.com"
        assert response.http_code == test_data["http_code"]

        mock_client.post_request.assert_called_once_with(
            endpoint=f"users/{test_data["user_name"]}/calendar/events",
            data={
                "subject": test_data["subject"],
                "body": {
                    "content": test_data["content"],
                },
                "start": {
                    "dateTime": test_data["start_date_time"],
                    "timeZone": test_data["time_zone"],
                },
                "end": {
                    "dateTime": test_data["end_date_time"],
                    "timeZone": test_data["time_zone"],
                },
                "location": {
                    "displayName": test_data["location"],
                },
                "attendees": [
                    {
                        "emailAddress": {"address": "john.doe@example.com", "name": "John Doe"},
                        "type": "required",
                    },
                ],
            },
        )
