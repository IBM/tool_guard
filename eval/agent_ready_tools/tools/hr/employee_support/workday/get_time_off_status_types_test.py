from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_time_off_status_types import (
    get_time_off_status_types,
)


def test_get_time_off_status_types() -> None:
    """Test that the `get_time_off_status_types` function returns the expected response."""

    # Define test data:
    test_data = {
        "status_type": "Approved",
        "type_id": "0391102bd1b542538d996936c8fa2fa7",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_time_off_status_types.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "id": test_data["type_id"],
                    "descriptor": test_data["status_type"],
                }
            ],
        }

        # Get time off status types
        response = get_time_off_status_types()

        # Ensure that get_time_off_status_types() executed and returned proper values
        assert response
        assert len(response.status_types)
        assert response.status_types[0].status_type == test_data["status_type"]
        assert response.status_types[0].type_id == test_data["type_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            url=f"api/absenceManagement/v1/{mock_client.tenant_name}/values/timeOff/status"
        )
