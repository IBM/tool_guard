from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.assign_recruiter import (
    assign_recruiter_to_job_requisition,
)


def test_assign_recruiter_to_job_requisition() -> None:
    """Test that `assign_recruiter_to_job_requisition` returns a success message."""
    test_data = {
        "job_requisition_id": "67979",
        "recruiter": "twalker",
        "expected_message": "The job requisition has been reassigned.",
    }

    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.assign_recruiter.get_sap_successfactors_client"
    ) as mock_sap_client:
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {"reassignJobReq": test_data["expected_message"]}
        }

        response = assign_recruiter_to_job_requisition(
            job_requisition_id=test_data["job_requisition_id"], recruiter=test_data["recruiter"]
        )

        assert response.message == test_data["expected_message"]

        mock_client.get_request.assert_called_once_with(
            entity="reassignJobReq",
            params={
                "jobReqId": test_data["job_requisition_id"],
                "recruiter": test_data["recruiter"],
                "$format": "json",
            },
        )
