from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.teams.update_an_event import update_an_event


def test_update_an_event() -> None:
    """Verifies that the event is updated successfully by the `update_an_event` tool."""

    # Create the test data
    test_data = {
        "event_id": "AAMkADYyODVkMjM5LTFlZTctNGYxZi1hOGM4LWFiZjYyNzlkMTk4NgBGAAAAAACc41e7EpqATZaoltx0URUoBwD-yalyWcFZS7k3FwN9Rv9bAAAAAAENAAD-yalyWcFZS7k3FwN9Rv9bAAbsMkSAAAA=",
        "start_datetime": "2025-03-15T12:00:00.0000000",
        "timezone": "Central Standard Time",
        "end_datetime": "2025-07-15T14:00:00.0000000",
        "user_name": "user@example.com",
    }

    output_subject = "Sung Jinwoo is having lunch"

    # Patch the microsoft client with the mock object
    with patch(
        "agent_ready_tools.tools.productivity.teams.update_an_event.get_microsoft_client"
    ) as mock_teams_client:

        # Create a mock client
        mock_client = MagicMock()
        mock_teams_client.return_value = mock_client
        mock_client.update_request.return_value = {
            "subject": output_subject,
            "start": {"dateTime": test_data["start_datetime"], "timeZone": test_data["timezone"]},
            "end": {"dateTime": test_data["end_datetime"], "timeZone": test_data["timezone"]},
        }
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        # Update an email
        response = update_an_event(
            event_id=test_data["event_id"],
            start_datetime=test_data["start_datetime"],
            end_datetime=test_data["end_datetime"],
            timezone=test_data["timezone"],
        )

        assert response
        assert response.event_subject == output_subject
        assert response.start_datetime == test_data["start_datetime"]
        assert response.start_timezone == test_data["timezone"]
        assert response.end_datetime == test_data["end_datetime"]
        assert response.end_timezone == test_data["timezone"]

        # Ensure the API call was made with expected parameters
        mock_client.update_request.assert_called_once_with(
            endpoint=f"users/{test_data["user_name"]}/calendar/events/{test_data["event_id"]}",
            data={
                "start": {
                    "dateTime": test_data["start_datetime"],
                    "timeZone": test_data["timezone"],
                },
                "end": {"dateTime": test_data["end_datetime"], "timeZone": test_data["timezone"]},
            },
        )
