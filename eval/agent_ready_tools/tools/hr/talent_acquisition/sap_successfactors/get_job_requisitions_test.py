from typing import Any, Dict
from unittest.mock import patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.get_job_requisitions import (
    get_job_requisitions,
)


def test_get_job_requisitions() -> None:
    """Test that the `get_job_requisitions` function returns the expected response."""

    test_data: Dict[str, Any] = {
        "job_req_id": "10001",
        "job_title": "Backend Developer",
        "status": "Open",
        "workflow_status": "APPROVED",
        "job_code": "DEV001",
        "posting_country": "India",
        "job_country_code": "IN",
        "job_grade": "G5",
        "job_start_date": "2025-07-07",
        "number_of_openings": "2",
        "business_unit": "Tech",
        "department": "Engineering",
        "division": "Product",
        "job_skill": "Python",
        "employment_type": "FT",
        "hiring_manager": "Alice Smith",
        "second_recruiter": "John Doe",
        "recruiter": "Jane Doe",
        "job_function": "DEV",
        "location": "Bangalore",
    }

    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.get_job_requisitions.get_sap_successfactors_client"
    ) as mock_sap_client:
        mock_client = mock_sap_client.return_value

        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "jobReqId": test_data["job_req_id"],
                        "internalStatus": test_data["workflow_status"],
                        "jobCode": test_data["job_code"],
                        "country": test_data["posting_country"],
                        "jobGrade": test_data["job_grade"],
                        "jobStartDate": test_data["job_start_date"],
                        "numberOpenings": test_data["number_of_openings"],
                        "status": {"results": [{"externalCode": test_data["status"]}]},
                        "businessUnit_obj": {"name": test_data["business_unit"]},
                        "department_obj": {"name": test_data["department"]},
                        "division_obj": {"name": test_data["division"]},
                        "filter1": {"results": [{"externalCode": test_data["job_country_code"]}]},
                        "jobskill": {"results": [{"externalCode": test_data["job_skill"]}]},
                        "filter3": {"results": [{"externalCode": test_data["employment_type"]}]},
                        "hiringManager": {"results": [{"firstName": "Alice", "lastName": "Smith"}]},
                        "secondRecruiter": {"results": [{"firstName": "John", "lastName": "Doe"}]},
                        "recruiter": {"results": [{"firstName": "Jane", "lastName": "Doe"}]},
                        "filter2": {"results": [{"mdfExternalCode": test_data["job_function"]}]},
                        "location_obj": {"results": [{"name": test_data["location"]}]},
                        "jobReqLocale": {"results": [{"jobTitle": test_data["job_title"]}]},
                    }
                ]
            }
        }

        response = get_job_requisitions(status_id="664496")

        assert response
        job = response.job_requisitions[0]

        assert job.job_req_id == test_data["job_req_id"]
        assert job.job_title == test_data["job_title"]
        assert job.status == test_data["status"]
        assert job.workflow_status == test_data["workflow_status"]
        assert job.job_code == test_data["job_code"]
        assert job.posting_country == test_data["posting_country"]
        assert job.job_country_code == test_data["job_country_code"]
        assert job.job_grade == test_data["job_grade"]
        assert job.number_of_openings == test_data["number_of_openings"]
        assert job.business_unit == test_data["business_unit"]
        assert job.department == test_data["department"]
        assert job.division == test_data["division"]
        assert job.job_skill == test_data["job_skill"]
        assert job.employment_type == test_data["employment_type"]
        assert job.hiring_manager == test_data["hiring_manager"]
        assert job.second_recruiter == test_data["second_recruiter"]
        assert job.recruiter == test_data["recruiter"]
        assert job.job_function == test_data["job_function"]
        assert job.location == test_data["location"]

        mock_client.get_request.assert_called_once_with(
            entity="JobRequisition",
            filter_expr="status/id eq '664496'",
            expand_expr=(
                "status,businessUnit_obj,department_obj,division_obj,"
                "filter1,jobskill,filter2,filter3,hiringManager,"
                "location_obj,secondRecruiter,jobReqLocale,recruiter"
            ),
            params={"$orderby": "jobReqId desc", "$top": 10, "$skip": 0},
        )
