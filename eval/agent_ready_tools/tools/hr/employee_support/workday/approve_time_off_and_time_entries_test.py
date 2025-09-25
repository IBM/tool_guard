from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.approve_time_off_and_time_entries import (
    approve_time_off_and_time_entries,
)


def test_approve_time_off_and_time_entries() -> None:
    """
    Test that the `approve_time_off_and_time_entries` function returns the expected response.

    WARNING: MANAGER Authentication Credentials Required
    """

    # Define test data:
    test_data = {
        "time_off_id": "0fdf3ec768f101004aa7360a4d11d300",
        "response": "denial",
        "descriptor": "Approval by Manager",
        "comment": "Money $$$$",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.approve_time_off_and_time_entries.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.approve_time_off_and_time_entries.return_value = {
            "descriptor": test_data["descriptor"],
        }

        # Deny time off
        response = approve_time_off_and_time_entries(
            pending_request_id=test_data["time_off_id"],
            request_response=test_data["response"],
            comment=test_data["comment"],
        )

        # Ensure that approve_time_off_and_time_entries() executed and returned proper values
        assert response
        assert response.descriptor == test_data["descriptor"]

        # Ensure the API call was made with expected parameters
        mock_client.approve_time_off_and_time_entries.assert_called_once_with(
            pending_request_id=test_data["time_off_id"],
            request_response=test_data["response"],
            payload={"comment": test_data["comment"]},
        )
