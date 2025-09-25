from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.request_time_off import (
    _request_time_off_payload,
    request_time_off,
)


def test_request_time_off() -> None:
    """Test that the `request_time_off` function returns the expected response."""

    # Define test data:
    test_data = {
        "user_id": "66def25413f74c13a90829e466a04f23",
        "start_date": "2025-09-01",
        "end_date": "2025-09-01",
        "time_off_type_id": "de52fbe58bc84c8b90883502f9f868ed",
        "default_daily_quantity": "8",
        "request_id": "3aa5550b7fe348b98d7b5741afc65534",
        "request_description": "Family business",
        "status": "Successfully Completed",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.request_time_off.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.request_time_off.return_value = {
            "businessProcessParameters": {
                "overallBusinessProcess": {
                    "id": test_data["request_id"],
                    "descriptor": test_data["request_description"],
                },
                "overallStatus": test_data["status"],
            },
            "days": [
                {
                    "date": test_data["start_date"],
                    "descriptor": test_data["request_description"],
                }
            ],
        }

        # Create TimeOff entry
        response = request_time_off(
            user_id=test_data["user_id"],
            time_off_start_date=test_data["start_date"],
            time_off_end_date=test_data["end_date"],
            time_off_type_id=test_data["time_off_type_id"],
            default_daily_quantity=test_data["default_daily_quantity"],
        )

        # Ensure that request_time_off() executed and returned proper values
        assert response
        assert response.request_id == test_data["request_id"]
        assert response.request_description == test_data["request_description"]
        assert response.request_status == test_data["status"]

        # Ensure the API calls was made with expected parameters
        mock_client.request_time_off.assert_called_once_with(
            test_data["user_id"],
            payload=_request_time_off_payload(
                time_off_start_date=test_data["start_date"],
                time_off_end_date=test_data["end_date"],
                time_off_type_id=test_data["time_off_type_id"],
                default_daily_quantity=test_data["default_daily_quantity"],
            ),
        )
