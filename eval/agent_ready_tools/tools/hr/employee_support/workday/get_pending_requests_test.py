from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_pending_requests import (
    get_pending_requests,
)


def test_get_pending_requests() -> None:
    """Test that the `get_pending_requests` function returns the expected response."""

    # Define test data:
    test_data = {
        "user_id": "fb151c22babd4004919999c601cc55a4",
        "pending_request_id": "b0a49483d1dd9000c590421152320001",
        "subject": "Adama Carlton",
        "assigned_date": "2025-03-24",
        "status": "Awaiting Action",
        "over_all_process": "Absence Request: Adama Carlton",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_pending_requests.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "assigned": test_data["assigned_date"],
                    "id": test_data["pending_request_id"],
                    "subject": {"descriptor": test_data["subject"]},
                    "descriptor": "",
                    "due": "2025-03-26",
                    "overallProcess": {"descriptor": test_data["over_all_process"]},
                    "status": {"descriptor": test_data["status"]},
                }
            ],
        }

        # Get pending requests
        response = get_pending_requests(user_id=test_data["user_id"])

        # Ensure that get_pending_requests() executed and returned proper values
        assert response
        assert len(response.pending_requests)
        assert response.pending_requests[0].pending_request_id == test_data["pending_request_id"]
        assert response.pending_requests[0].subject == test_data["subject"]
        assert response.pending_requests[0].over_all_process == test_data["over_all_process"]
        assert response.pending_requests[0].assigned_date == test_data["assigned_date"]
        assert response.pending_requests[0].status == test_data["status"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            url=f"api/common/v1/{mock_client.tenant_name}/workers/{test_data['user_id']}/inboxTasks"
        )
