from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.upsert_job_description import (
    upsert_job_description,
)


def test_upsert_job_description() -> None:
    """Tests that the job description is upserting successfully using the `upsert_job_description`
    tool."""

    # Define test data
    test_data = {
        "job_requisition_id": "67589",
        "internal_job_description": "A Software Engineer designs, develops, and maintains software applications to meet user needs and ensure system functionality.",
        "external_job_description": "Automation is mandatory.",
        "location_obj": "6200-0001",
        "legalEntity_obj": "4000",
        "response_http_code": 204,
        "response_message": "Job Requisition has been updated successfully",
    }

    # Patch both get_sap_successfactors_client and get_job_requisition
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.upsert_job_description.get_sap_successfactors_client"
    ) as mock_sap_client, patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.upsert_job_description.get_job_requisition"
    ) as mock_get_job_requisition:

        # Mock job requisition response
        mock_get_job_requisition.return_value = MagicMock(
            location=test_data["location_obj"],
            company=test_data["legalEntity_obj"],
        )

        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.upsert_request.return_value = {
            "d": [
                {
                    "httpCode": test_data["response_http_code"],
                    "message": test_data["response_message"],
                }
            ]
        }

        # Upsert job description
        response = upsert_job_description(
            job_requisition_id=test_data["job_requisition_id"],
            external_job_description=test_data["external_job_description"],
            internal_job_description=test_data["internal_job_description"],
        )

        # Ensure that upsert_job_description() executed and returned proper values
        assert response
        assert response.http_code == test_data["response_http_code"]
        assert response.message == test_data["response_message"]

        # Ensure the API call was made with expected parameters
        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {
                    "uri": "JobRequisition",
                    "type": "SFOData.JobRequisition",
                },
                "jobReqId": test_data["job_requisition_id"],
                "jobReqLocale": {
                    "jobDescription": test_data["internal_job_description"],
                    "externalJobDescription": test_data["external_job_description"],
                },
                "location_obj": {"externalCode": test_data["location_obj"]},
                "legalEntity_obj": {"externalCode": test_data["legalEntity_obj"]},
            }
        )
