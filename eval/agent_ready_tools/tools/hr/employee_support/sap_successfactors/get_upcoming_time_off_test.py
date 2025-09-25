from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_upcoming_time_off import (
    get_upcoming_time_off,
)
from agent_ready_tools.utils.format_tool_input import string_to_list_of_strings


def test_get_upcoming_time_off() -> None:
    """Test that the `get_upcoming_time_off` function returns the expected response."""
    # Define test data:
    test_data = {
        "user_id": "100052",
        "start_date": "2025-01-01",
        "end_date": "2025-01-01",
        "title": "New Year's Day",
        "type": "['PUBLIC_HOLIDAY']",
        "time_unit": "DAYS",
        "duration": 1,
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_upcoming_time_off.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_time_management_request.return_value = {
            "value": [
                {
                    "title": test_data["title"],
                    "type": test_data["type"],
                    "startDate": test_data["start_date"],
                    "endDate": test_data["end_date"],
                    "duration": test_data["duration"],
                    "timeUnit": test_data["time_unit"],
                }
            ]
        }

        # Get upcoming TimeOff
        response = get_upcoming_time_off(
            user_id=test_data["user_id"],
            start_date=test_data["start_date"],
            end_date=test_data["end_date"],
            time_off_types=test_data["type"],
        )

        # Ensure that get_upcoming_time_off() executed and returned proper values
        assert response
        assert len(response.time_off_events)
        assert response.time_off_events[0].title == test_data["title"]
        assert response.time_off_events[0].start_date == test_data["start_date"]
        assert response.time_off_events[0].end_date == test_data["end_date"]
        assert response.time_off_events[0].type == test_data["type"]
        assert response.time_off_events[0].time_unit == test_data["time_unit"]
        assert response.time_off_events[0].duration == test_data["duration"]

        # Ensure the API call was made with expected parameters
        mock_client.get_time_management_request.assert_called_once_with(
            endpoint="events",
            params={
                "assignmentId": test_data["user_id"],
                "types": string_to_list_of_strings(str(test_data["type"])),
                "startDate": test_data["start_date"],
                "endDate": test_data["end_date"],
            },
        )
