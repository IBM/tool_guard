from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.get_applicants_for_job_requisition import (
    get_all_applicants,
)


def test_get_all_applicants() -> None:
    """Test that the `get_all_applicants` function returns the expected response."""

    test_data = {
        "application_id": "388",
        "first_name": "Marcelo",
        "last_name": "Reis",
        "country": "Brazil",
        "job_req_id": "207",
        "contact_email": "test@abc.com",
        "cell_phone": "+5511 9999-9999",
        "job_requisition_id": "207",
        "city": "São Paulo",
        "candidate_id": "1467",
    }

    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.get_applicants_for_job_requisition.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "applicationId": "388",
                        "firstName": "Marcelo",
                        "lastName": "Reis",
                        "country": "Brazil",
                        "jobReqId": "207",
                        "contactEmail": "test@abc.com",
                        "cellPhone": "+5511 9999-9999",
                        "city": "São Paulo",
                        "candidateId": "1467",
                    },
                ]
            }
        }

        response = get_all_applicants(job_requisition_id=test_data["job_requisition_id"])

        assert response

        mock_client.get_request.assert_called_once_with(
            entity="JobApplication",
            filter_expr=f"jobReqId eq {test_data["job_requisition_id"]}",
        )
