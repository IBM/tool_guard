from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.approve_request_details import (
    approve_request_details,
)


def test_approve_request_details() -> None:
    """Test that the approval request for a user was successfully approved or rejected by the
    approve_request_details tool."""
    # Define test data:
    test_data = {
        "workflow_id": "109031",
        "workflow_status": "approve",
        "request_status": "success",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.approve_request_details.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.post_request.return_value = {"d": [{"status": test_data["request_status"]}]}

        # Approve the request
        response = approve_request_details(
            workflow_request_id=test_data["workflow_id"], status=test_data["workflow_status"]
        )

        # Ensure that approve_request_details() executed and returned proper values
        assert response
        assert response.status == test_data["request_status"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="approveWfRequest",
            params={"wfRequestId": f"{test_data['workflow_id']}L"},
        )
