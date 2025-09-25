from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_all_pending_requests import (
    get_all_pending_requests,
)


def test_get_all_pending_requests() -> None:
    """Test that pending approvals for employees can be retrieved successfully."""
    # Define test data:
    test_data = {
        "user_id": "103343",
        "status": "PENDING",
        "wf_request_id": "3213941381",
        "request_type": "empWfRequestNav",
        "created_on": "2025-01-01",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_all_pending_requests.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "wfRequestId": test_data["wf_request_id"],
                        "status": test_data["status"],
                        "empWfRequestNav": {
                            "requestType": test_data["request_type"],
                            "jobInfoNav": {"results": [{"userId": test_data["user_id"]}]},
                        },
                        "createdOn": test_data["created_on"],
                    },
                ]
            }
        }

        # Get all pending requests
        response = get_all_pending_requests(user_id=test_data["user_id"]).pending_requests[0]

        # Ensure that get_all_pending_requests() executed and returned proper values
        assert response
        assert response.status == test_data["status"]
        assert response.wf_request_id == test_data["wf_request_id"]
        assert response.request_type == test_data["request_type"]
        assert response.created_on == test_data["created_on"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="WfRequest",
            filter_expr=f"status eq '{test_data['status']}' and empWfRequestNav/jobInfoNav/userId eq '{test_data['user_id']}'",
            expand_expr="empWfRequestNav,empWfRequestNav/jobInfoNav,empWfRequestNav/jobInfoNav/userNav",
        )
