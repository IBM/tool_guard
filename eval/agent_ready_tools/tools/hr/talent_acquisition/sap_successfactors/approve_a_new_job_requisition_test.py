from unittest.mock import MagicMock, patch

from requests import HTTPError
from requests.models import Response

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.approve_a_new_job_requisition import (
    approve_a_new_job_requisition,
)


def test_approve_job_requisition_success() -> None:
    """Tests that a job requisition can be successfully approved by the
    `approve_a_new_job_requisition` tool."""

    # Define test data:
    test_data = {
        "job_requisition_id": "68017",
        "comments": "Approved by manager",
        "message": "Job requisition approved successfully.",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.approve_a_new_job_requisition.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "d": {"approveOrDeclineJobReqForm": test_data["message"]}
        }

        # Approve job requisition
        response = approve_a_new_job_requisition(
            job_requisition_id=test_data["job_requisition_id"],
            comments=test_data["comments"],
        )

        # Ensure that approve_a_new_job_requisition() executed and returned proper values
        assert response
        assert response.message == test_data["message"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="approveOrDeclineJobReqForm",
            params={
                "jobReqId": f"{test_data['job_requisition_id']}L",
                "comments": test_data["comments"],
                "actionType": "'APPROVE'",
            },
        )


def test_approve_job_requisition_http_error() -> None:
    """Tests that job requisition approval handles HTTPError with nested error message properly."""

    # Define test data:
    test_data = {
        "job_requisition_id": "67991",
        "error_message": "[COE0019]Exception while approving the job req:67991 INVALID_FORM_STATUS",
        "http_code": 500,
    }

    # Create a mock response object
    mock_response = MagicMock(spec=Response)
    mock_response.status_code = test_data["http_code"]
    mock_response.json.return_value = {
        "error": {
            "code": "COE_GENERAL_SERVER_FAILURE",
            "message": {
                "lang": "en-US",
                "value": test_data["error_message"],
            },
        }
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.approve_a_new_job_requisition.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.post_request.side_effect = HTTPError(response=mock_response)

        # Approve job requisition
        response = approve_a_new_job_requisition(test_data["job_requisition_id"])

        # Ensure that approve_a_new_job_requisition() executed and returned proper values
        assert response
        assert response.message == test_data["error_message"]
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="approveOrDeclineJobReqForm",
            params={
                "jobReqId": f"{test_data['job_requisition_id']}L",
                "actionType": "'APPROVE'",
            },
        )
