from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.outlook.create_outlook_event import create_outlook_event


def test_create_outlook_event() -> None:
    """Verify that the `create_outlook_event` tool can successfully create a simple Outlook
    event."""

    # Define test data:
    test_data = {
        "event_id": "987654321",
        "subject": "Creating an Outlook event",
        "attendees": "sample@email.com",
        "start_date_time": "2025-03-24T12:00:00",
        "end_date": "2025-03-24T13:00:00",
        "timezone": "UTC",
        "location": "Armii Krajowej, Krakow",
        "user_name": "user@example.com",
        "content": "Simple event content",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.outlook.create_outlook_event.get_microsoft_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.post_request.return_value = {"id": test_data["event_id"]}
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        # Create Microsoft Outlook Event
        response = create_outlook_event(
            subject=test_data["subject"],
            content=test_data["content"],
            start_date_time=f"{test_data['start_date_time']} {test_data['timezone']}",
            duration="60",
            attendees=test_data["attendees"],
            is_online_event=False,
            location=test_data["location"],
        )

        # Ensure that update_a_comment() executed and returned proper values
        assert response
        assert response.event_id == test_data["event_id"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint=f"users/{test_data["user_name"]}/events",
            data={
                "subject": test_data["subject"],
                "body": {"content": test_data["content"], "contentType": "HTML"},
                "start": {
                    "dateTime": test_data["start_date_time"],
                    "timeZone": test_data["timezone"],
                },
                "end": {
                    "dateTime": test_data["end_date"],
                    "timeZone": test_data["timezone"],
                },
                "attendees": [
                    {
                        "emailAddress": {"address": test_data["attendees"]},
                        "type": "required",
                    }
                ],
                "isOnlineMeeting": False,
                "location": {"displayName": test_data["location"]},
            },
        )


def test_create_recurring_outlook_event() -> None:
    """Verify that the `create_outlook_event` tool can successfully create a recurring Outlook
    event."""

    # Define test data:
    test_data = {
        "event_id": "rec123456789",
        "subject": "Weekly Team Sync",
        "attendees": "dev@example.com,qa@example.com",
        "start_date_time": "2025-07-01T10:00:00",
        "end_date": "2025-07-01T10:45:00",
        "timezone": "UTC",
        "location": "Virtual Room",
        "user_name": "user@example.com",
        "content": "Recurring event content",
        "recurrence_type": "Weekly",
        "frequency": 1,
        "days_of_the_week": "Monday,Friday",
        "recurrence_end_date": "2025-08-30",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.outlook.create_outlook_event.get_microsoft_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.post_request.return_value = {"id": test_data["event_id"]}
        mock_client.get_user_resource_path.return_value = f"users/{test_data['user_name']}"

        # Create Microsoft Recurring Outlook Event
        response = create_outlook_event(
            subject=test_data["subject"],
            content=test_data["content"],
            start_date_time=f"{test_data['start_date_time']} {test_data['timezone']}",
            duration="45",
            attendees=test_data["attendees"],
            is_online_event=False,
            location=test_data["location"],
            recurrence_type=test_data["recurrence_type"],
            frequency=test_data["frequency"],
            days_of_the_week=test_data["days_of_the_week"],
            recurrence_end_date=test_data["recurrence_end_date"],
        )

        # Ensure that update_a_comment() executed and returned proper values
        assert response
        assert response.event_id == test_data["event_id"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint=f"users/{test_data['user_name']}/events",
            data={
                "subject": test_data["subject"],
                "body": {"content": test_data["content"], "contentType": "HTML"},
                "start": {
                    "dateTime": test_data["start_date_time"],
                    "timeZone": test_data["timezone"],
                },
                "end": {
                    "dateTime": test_data["end_date"],
                    "timeZone": test_data["timezone"],
                },
                "attendees": [
                    {"emailAddress": {"address": "dev@example.com"}, "type": "required"},
                    {"emailAddress": {"address": "qa@example.com"}, "type": "required"},
                ],
                "isOnlineMeeting": False,
                "location": {"displayName": test_data["location"]},
                "recurrence": {
                    "pattern": {
                        "type": "weekly",
                        "interval": 1,
                        "daysOfWeek": ["Monday", "Friday"],
                    },
                    "range": {
                        "type": "endDate",
                        "startDate": "2025-07-01",
                        "endDate": test_data["recurrence_end_date"],
                    },
                },
            },
        )
