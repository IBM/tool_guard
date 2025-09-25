from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.outlook.get_all_events import get_all_events


def test_get_all_events() -> None:
    """Test retrieving all events without filters."""
    test_data = {
        "id": "987654321",
        "subject": "Stand-up",
        "start_time": "2025-07-01T12:00:00",
        "end_time": "2025-07-01T13:00:00",
    }

    with patch(
        "agent_ready_tools.tools.productivity.outlook.get_all_events.get_microsoft_client"
    ) as mock_box_client:
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.get_user_resource_path.return_value = "me"
        mock_client.get_request.return_value = {
            "value": [
                {
                    "id": test_data["id"],
                    "subject": test_data["subject"],
                    "start": {"dateTime": test_data["start_time"]},
                    "end": {"dateTime": test_data["end_time"]},
                }
            ]
        }

        response = get_all_events()

        assert response
        assert len(response.events) == 1
        assert response.events[0].id == test_data["id"]
        assert response.events[0].subject == test_data["subject"]
        assert response.events[0].start_time == test_data["start_time"]
        assert response.events[0].end_time == test_data["end_time"]

        mock_client.get_request.assert_called_once_with(
            endpoint="me/events?$select=subject,start,end", params={}
        )


def test_get_events_by_subject() -> None:
    """Test filtering events by subject."""
    test_data = {
        "id": "987654321",
        "subject": "Stand-up",
        "start_time": "2025-07-01T12:00:00",
        "end_time": "2025-07-01T13:00:00",
    }
    with patch(
        "agent_ready_tools.tools.productivity.outlook.get_all_events.get_microsoft_client"
    ) as mock_box_client:
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.get_user_resource_path.return_value = "me"
        mock_client.get_request.return_value = {
            "value": [
                {
                    "id": test_data["id"],
                    "subject": test_data["subject"],
                    "start": {"dateTime": test_data["start_time"]},
                    "end": {"dateTime": test_data["end_time"]},
                }
            ]
        }

        response = get_all_events(event_subject="Stand-up")

        assert response
        assert len(response.events) == 1
        assert response.events[0].id == test_data["id"]
        assert response.events[0].subject == test_data["subject"]
        assert response.events[0].start_time == test_data["start_time"]
        assert response.events[0].end_time == test_data["end_time"]

        mock_client.get_request.assert_called_once_with(
            endpoint="me/events?$select=subject,start,end",
            params={"$filter": f"subject eq '{test_data['subject']}'"},
        )


def test_get_events_by_start_date() -> None:
    """Test filtering events by start date."""
    test_data = {
        "id": "987654321",
        "subject": "Stand-up",
        "start_time": "2025-07-01T12:00:00",
        "end_time": "2025-07-01T13:00:00",
    }
    with patch(
        "agent_ready_tools.tools.productivity.outlook.get_all_events.get_microsoft_client"
    ) as mock_box_client:
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.get_user_resource_path.return_value = "me"
        mock_client.get_request.return_value = {
            "value": [
                {
                    "id": test_data["id"],
                    "subject": test_data["subject"],
                    "start": {"dateTime": test_data["start_time"]},
                    "end": {"dateTime": test_data["end_time"]},
                }
            ]
        }

        response = get_all_events(start_date_time="2025-07-01T12:00:00")

        assert response
        assert len(response.events) == 1
        assert response.events[0].id == test_data["id"]
        assert response.events[0].subject == test_data["subject"]
        assert response.events[0].start_time == test_data["start_time"]
        assert response.events[0].end_time == test_data["end_time"]

        mock_client.get_request.assert_called_once_with(
            endpoint="me/events?$select=subject,start,end",
            params={"$filter": f"start/dateTime ge '{test_data['start_time']}'"},
        )


def test_get_events_by_end_date() -> None:
    """Test filtering events by end date."""
    test_data = {
        "id": "987654321",
        "subject": "Stand-up",
        "start_time": "2025-07-01T12:00:00",
        "end_time": "2025-07-01T13:00:00",
    }
    with patch(
        "agent_ready_tools.tools.productivity.outlook.get_all_events.get_microsoft_client"
    ) as mock_box_client:
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.get_user_resource_path.return_value = "me"
        mock_client.get_request.return_value = {
            "value": [
                {
                    "id": test_data["id"],
                    "subject": test_data["subject"],
                    "start": {"dateTime": test_data["start_time"]},
                    "end": {"dateTime": test_data["end_time"]},
                }
            ]
        }

        response = get_all_events(end_date_time="2025-07-01T13:00:00")

        assert response
        assert len(response.events) == 1
        assert response.events[0].id == test_data["id"]
        assert response.events[0].subject == test_data["subject"]
        assert response.events[0].start_time == test_data["start_time"]
        assert response.events[0].end_time == test_data["end_time"]

        mock_client.get_request.assert_called_once_with(
            endpoint="me/events?$select=subject,start,end",
            params={"$filter": f"end/dateTime le '{test_data['end_time']}'"},
        )
