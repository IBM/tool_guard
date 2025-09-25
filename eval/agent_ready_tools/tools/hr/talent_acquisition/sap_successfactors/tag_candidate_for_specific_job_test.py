from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.tag_candidate_for_specific_job import (
    tag_candidate_for_specific_job,
)


def test_tag_candidate_for_specific_job() -> None:
    """Verify that the `tag_candidate_for_specific_job` tool can successfully tag a candidate for a
    specific job."""
    # Define test data:
    test_data = {
        "job_requisition_id": "67943",
        "candidate_id": "6044",
        "http_code": 201,
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.tag_candidate_for_specific_job.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.post_request.return_value = {"http_code": test_data["http_code"]}

        # Tag a candidate for a specific job
        response = tag_candidate_for_specific_job(
            job_requisition_id=test_data["job_requisition_id"],
            candidate_id=test_data["candidate_id"],
        )

        # Ensure that tag_candidate_for_specific_job() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="JobReqFwdCandidates",
            payload={
                "__metadata": {
                    "uri": "JobReqFwdCandidates",
                    "type": "SFOData.JobReqFwdCandidates",
                },
                "jobReqId": test_data["job_requisition_id"],
                "candidateId": test_data["candidate_id"],
                "status": "Default",
            },
        )
