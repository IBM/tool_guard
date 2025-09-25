from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.create_job_requisition import (
    create_job_requisition,
)


def test_create_job_requisition() -> None:
    """Tests that the `create_job_requisition` function returns the expected response."""
    # Define test data:
    test_data: Dict[str, Any] = {
        "http_code": 201,
        "message": "Job Requisition has been inserted successfully",
        "template_id": "1796",
        "country": "India",
        "posting_country": "India",
        "company_code": "4000",
        "job_start_date": "2025-07-18",
        "number_of_openings": "1",
        "employee_type": "3979",
        "job_function_code": "11969",
        "state": "11640",
        "location_code": "6200-0001",
        "hiring_manager_id": "82094",
        "recruiter_manager_id": "82094",
        "internal_job_title": "testing from agent",
        "external_job_title": "testing from tool code",
        "custom_fields": {
            "jobskill": {"key": "id", "value": "664380", "type": "picklist"},
            "jobGrade": {"value": "A1", "type": "enum"},
            "secondRecruiter": {"key": "userName", "value": "twalker", "type": "object"},
        },
        "posting_country_code": "5582",
        "sap_date": "/Date(1752796800000)/",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.create_job_requisition.get_sap_successfactors_client"
    ) as mock_sap_client, patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.create_job_requisition.get_country_code"
    ) as mock_get_country_code, patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.create_job_requisition.iso_8601_to_sap_date"
    ) as mock_iso_8601_to_sap_date:

        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.upsert_request.return_value = {
            "d": [{"message": test_data["message"], "httpCode": test_data["http_code"]}]
        }

        mock_get_country_code.return_value = test_data["posting_country_code"]
        mock_iso_8601_to_sap_date.return_value = test_data["sap_date"]

        response = create_job_requisition(
            template_id=test_data["template_id"],
            country=test_data["country"],
            posting_country=test_data["posting_country"],
            company_code=test_data["company_code"],
            job_start_date=test_data["job_start_date"],
            number_of_openings=test_data["number_of_openings"],
            employee_type=test_data["employee_type"],
            job_function_code=test_data["job_function_code"],
            state=test_data["state"],
            location_code=test_data["location_code"],
            hiring_manager_id=test_data["hiring_manager_id"],
            recruiter_manager_id=test_data["recruiter_manager_id"],
            internal_job_title=test_data["internal_job_title"],
            external_job_title=test_data["external_job_title"],
            custom_fields=test_data["custom_fields"],
        )

        # Ensure that create_job_requisition executed and returned proper values
        assert response
        assert response.message == test_data["message"]
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {"uri": "JobRequisition", "type": "SFOData.JobRequisition"},
                "templateId": test_data["template_id"],
                "legalEntity_obj": {"externalCode": test_data["company_code"]},
                "country": test_data["country"],
                "jobStartDate": test_data["sap_date"],
                "numberOpenings": test_data["number_of_openings"],
                "filter2": {"id": test_data["job_function_code"]},
                "filter1": {"id": test_data["posting_country_code"]},
                "filter3": {"id": test_data["employee_type"]},
                "state": {"id": test_data["state"]},
                "location_obj": {"externalCode": test_data["location_code"]},
                "hiringManager": {"usersSysId": test_data["hiring_manager_id"]},
                "recruiter": {"usersSysId": test_data["recruiter_manager_id"]},
                "jobReqLocale": {
                    "jobTitle": test_data["internal_job_title"],
                    "externalTitle": test_data["external_job_title"],
                },
                "jobskill": {"id": "664380"},
                "jobGrade": "A1",
                "secondRecruiter": {"userName": "twalker"},
            }
        )
