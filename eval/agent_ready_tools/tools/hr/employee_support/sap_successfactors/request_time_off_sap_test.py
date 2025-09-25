from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.request_time_off_sap import (
    request_time_off_sap,
)
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date


def test_request_time_off_sap() -> None:
    """Test that the `request_time_off_sap` function returns the expected response."""
    # Define test data:
    test_data = {
        "user_id": "103362",
        "time_type": "TRAVEL",
        "start_date": "2025-09-20",
        "end_date": "2025-09-30",
        "request_id": "123213",
        "status_code": 200,
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.request_time_off_sap.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.upsert_request.return_value = {
            "d": [{"key": test_data["request_id"], "httpCode": test_data["status_code"]}]
        }

        # Create the time off request
        response = request_time_off_sap(
            user_id=test_data["user_id"],
            time_type=test_data["time_type"],
            start_date=test_data["start_date"],
            end_date=test_data["end_date"],
        )
        # Ensure that request_time_off_sap() executed and returned proper values
        assert response
        assert response.request_id == test_data["request_id"]

        # Ensure the API call was made with expected parameters
        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {"uri": "EmployeeTime", "type": "SFOData.EmployeeTime"},
                "startDate": iso_8601_to_sap_date(str(test_data["start_date"])),
                "endDate": iso_8601_to_sap_date(str(test_data["end_date"])),
                "userIdNav": {
                    "__metadata": {"uri": f"User('{test_data['user_id']}')", "type": "SFOData.User"}
                },
                "timeTypeNav": {
                    "__metadata": {
                        "uri": f"TimeType('{test_data['time_type']}')",
                        "type": "SFOData.TimeType",
                    }
                },
            },
        )
