from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.outlook.get_schedule_times import get_schedule_times


def test_get_schedule_times() -> None:
    """Verify that the `get_schedule_times` tool can successfully return schedule times from
    Microsoft Outlook."""

    # Define test data:
    test_data = {
        "email_address": "cstest@ibmappcon.onmicrosoft.com",
        "start_date_time": "2025-03-29T08:00:00",
        "time_zone": "India Standard Time",
        "end_date_time": "2025-03-29T17:00:00",
        "user_name": "user@example.com",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.outlook.get_schedule_times.get_microsoft_client"
    ) as mock_outlook_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_outlook_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "value": [
                {
                    "scheduleItems": [
                        {
                            "status": "busy",
                            "start": {"dateTime": "2025-03-28T06:30:00.0000000"},
                            "end": {"dateTime": "2025-03-28T07:00:00.0000000"},
                        }
                    ],
                }
            ],
        }
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        response = get_schedule_times(
            email_address=test_data["email_address"],
            start_date_time=test_data["start_date_time"],
            time_zone=test_data["time_zone"],
            end_date_time=test_data["end_date_time"],
        )

        # Ensure that get_schedule_times() executed and returned proper values
        assert response
        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint=f"users/{test_data["user_name"]}/calendar/getSchedule",
            headers={"Prefer": f'outlook.timezone ="{test_data["time_zone"]}"'},
            data={
                "schedules": [test_data["email_address"]],
                "startTime": {
                    "dateTime": test_data["start_date_time"],
                    "timeZone": test_data["time_zone"],
                },
                "endTime": {
                    "dateTime": test_data["end_date_time"],
                    "timeZone": test_data["time_zone"],
                },
            },
        )
