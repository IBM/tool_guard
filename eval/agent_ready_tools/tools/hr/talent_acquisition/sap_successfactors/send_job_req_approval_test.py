from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.send_job_req_approval import (
    send_job_req_approval,
)


def test_search_states_by_country() -> None:
    """Test that the `send_job_req_approval` function returns the expected response."""

    # Define test data:
    test_data = {
        "job_requisition_id": "67982",
        "comments": "Testing hello comments.",
        "message": "The job requisition has been sent to next step.",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.send_job_req_approval.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "d": {"sendJobReqToNextStep": test_data["message"]}
        }

        # Send a job requisition for approval
        response = send_job_req_approval(
            job_requisition_id="67982",
            comments="Testing hello comments.",
        )

        # Ensure that send_job_req_approval() executed and returned proper values
        assert response
        assert response.message == test_data["message"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="sendJobReqToNextStep",
            params={
                "jobReqId": f"{test_data["job_requisition_id"]}L",
                "comments": test_data["comments"],
            },
        )
