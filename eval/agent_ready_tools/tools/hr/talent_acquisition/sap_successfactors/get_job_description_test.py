from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.get_job_description import (
    get_job_description,
)


def test_get_job_description_success() -> None:
    """Test that the `get_job_description` function returns the expected response."""
    # Define test data:
    test_data = {
        "hiring_manager_user_id": "82094",
        "recruiter_user_id": "WORPABOT11",
        "job_requisition_id": "68021",
        "top": "5",
        "skip": "0",
        "external_job_description": "test1 by aqheel sharan1 final",
        "internal_job_description": "test2 by aqheel sharan2 final",
        "job_title": "Testing TA Flow vs",
    }
    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.get_job_description.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "jobReqId": test_data["job_requisition_id"],
                        "jobTitle": test_data["job_title"],
                        "jobDescription": test_data["internal_job_description"],
                        "externalJobDescription": test_data["external_job_description"],
                    }
                ]
            }
        }

        response = get_job_description(
            hiring_manager_user_id=test_data["hiring_manager_user_id"],
            recruiter_user_id=test_data["recruiter_user_id"],
            job_requisition_id=test_data["job_requisition_id"],
            top=test_data["top"],
            skip=test_data["skip"],
        )

        job_desc = response.job_descriptions[0]
        assert job_desc.job_requisition_id == test_data["job_requisition_id"]
        assert job_desc.job_title == test_data["job_title"]
        assert job_desc.external_job_description == test_data["external_job_description"]
        assert job_desc.internal_job_description == test_data["internal_job_description"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="JobRequisitionLocale",
            filter_expr="jobReqId eq '68021' and hiringManager/usersSysId eq '82094' and recruiter/usersSysId eq 'WORPABOT11'",
            select_expr="externalJobDescription,jobDescription,jobTitle,jobReqId",
            params={
                "$orderby": "jobReqId desc",
                "$top": test_data["top"],
                "$skip": test_data["skip"],
            },
        )
